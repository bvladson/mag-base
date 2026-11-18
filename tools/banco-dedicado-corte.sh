#!/bin/sh
# Corte do banco do sistema de tarefas (executado uma vez em 28/09/2026):
#   instância MariaDB compartilhada (3306, banco leantime_task, junto com BIomie e Criativo em Tela)
#   -> instância exclusiva mariadb@tarefas (127.0.0.1:3307, banco mag_tarefas).
# Pré-requisitos: /etc/mysql/mariadb.conf.d/99-tarefas.cnf, serviço mariadb@tarefas ativo,
# banco mag_tarefas vazio e usuário mag_tarefas@127.0.0.1 com senha em /root/mag-base/db/.mag_tarefas.pw.
# O sistema fica indisponível alguns segundos (usuário antigo bloqueado durante a cópia).
set -eu
umask 077

D=/root/mag-base/db
ENV=/var/www/leantime/shared/.env
PW=$(cat "$D/.mag_tarefas.pw")
NOVA="--defaults-group-suffix=.tarefas"
OPTS_DADOS="--no-create-info --skip-triggers --order-by-primary --skip-dump-date --skip-comments --skip-extended-insert --compact"

# 0. Pré-condições
[ "$(mariadb $NOVA -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='mag_tarefas'")" = 0 ]
grep -q "^LEAN_DB_DATABASE='leantime_task'$" "$ENV"

# 1. Backup completo pelo script oficial (banco antigo + arquivos)
/usr/local/sbin/leantime-backup

# 2. Bloqueia o usuário antigo e encerra as conexões dele
mariadb -e "ALTER USER 'leantime_task'@'localhost' ACCOUNT LOCK"
for id in $(mariadb -N -e "SELECT id FROM information_schema.processlist WHERE user='leantime_task'"); do
    mariadb -e "KILL $id" || true
done

# 3. Copia
mariadb-dump --single-transaction --quick --routines --triggers --events leantime_task > "$D/corte.sql"
mariadb $NOVA mag_tarefas < "$D/corte.sql"

# 4. Compara tabelas e dados (dumps só de dados, ordenados pela chave primária)
TA=$(mariadb -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='leantime_task'")
TB=$(mariadb $NOVA -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='mag_tarefas'")
A=$(mariadb-dump $OPTS_DADOS leantime_task | sha256sum | cut -d' ' -f1)
B=$(mariadb-dump $NOVA $OPTS_DADOS mag_tarefas | sha256sum | cut -d' ' -f1)
echo "tabelas: $TA -> $TB"
echo "dados:   $A"
echo "         $B"
if [ "$A" != "$B" ] || [ "$TA" != "$TB" ]; then
    echo "DIVERGÊNCIA: usuário antigo desbloqueado, configuração não alterada" >&2
    mariadb -e "ALTER USER 'leantime_task'@'localhost' ACCOUNT UNLOCK"
    exit 1
fi

# 5. Aponta o sistema para a instância exclusiva
cp -p "$ENV" "$D/env.antes-banco"
sed -i \
    -e "s|^LEAN_DB_HOST=.*|LEAN_DB_HOST='127.0.0.1'|" \
    -e "s|^LEAN_DB_PORT=.*|LEAN_DB_PORT='3307'|" \
    -e "s|^LEAN_DB_DATABASE=.*|LEAN_DB_DATABASE='mag_tarefas'|" \
    -e "s|^LEAN_DB_USER=.*|LEAN_DB_USER='mag_tarefas'|" \
    -e "s|^LEAN_DB_PASSWORD=.*|LEAN_DB_PASSWORD='$PW'|" \
    "$ENV"
systemctl reload php8.3-fpm
cd /var/www/leantime/current
runuser -u leantime -- php bin/leantime cache:clear installation >/dev/null

grep -E "^LEAN_DB_(HOST|PORT|DATABASE|USER)=" "$ENV"
curl -s -o /dev/null -w "login %{http_code}\n" --resolve task.magmoveiscorporativos.com.br:443:127.0.0.1 \
    https://task.magmoveiscorporativos.com.br/auth/login
echo "Reverter: cp -p $D/env.antes-banco $ENV && mariadb -e \"ALTER USER 'leantime_task'@'localhost' ACCOUNT UNLOCK\" && systemctl reload php8.3-fpm"
