"""Trocas exatas de texto no overlay (marca Leantime → MAG / neutro).

Cada trecho precisa aparecer exatamente uma vez no arquivo; se o arquivo já tiver
sido trocado, o script avisa e segue (idempotente). Identificadores de código
(namespaces, variáveis $leantime*, window.leantime) não são tocados.
"""
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / 'overlay' / 'app'

TROCAS = {
    'Domain/Connector/Templates/integrationEntity.blade.php': [
        ("On this screen you can choose what you would like to synchronize. Choose an entity on the left and map it to someting in Leantime on the right.",
         "Nesta tela você escolhe o que deseja sincronizar. Selecione uma entidade à esquerda e associe-a a um item do sistema à direita."),
        ("<h1>To (Leantime)</h1>", "<h1>Para (MAG)</h1>"),
        ('<label for="leantimeEntities">Leantime</label>', '<label for="leantimeEntities">MAG</label>'),
    ],
    'Domain/Connector/Templates/integrationFields.blade.php': [
        ("Match the fields from your source to the corresponding fields in Leantime",
         "Associe os campos da origem aos campos correspondentes no sistema"),
        ('<th class="center">Leantime Field</th>', '<th class="center">Campo no sistema</th>'),
    ],
    'Domain/Connector/Templates/show.blade.php': [
        ("Sync Leantime with your external applications", "Sincronize o sistema com suas aplicações externas"),
    ],
    'Domain/Auth/Templates/userInvite5.blade.php': [
        ("🎉 Your Leantime journey is about to begin", "🎉 Tudo pronto para começar"),
    ],
    # Modais de ajuda (blueprints, projectDashboard…): traduzidos por traduzir_ajuda.py
    'Domain/CsvImport/Templates/upload.blade.php': [
        ('<p>You can upload CSVs to import or update Tasks, Projects, Goals. <a href="https://support.leantime.io/importing-data-via-csv" target="_blank">Check our documentation</a> to learn more about the formatting and to download templates</p>',
         '<p>Envie arquivos CSV para importar ou atualizar Tarefas, Projetos e Metas.</p>'),
    ],
    'Domain/CsvImport/Services/CsvImport.php': [
        ("\"Import data from a CSV file. To learn more about the CSV format, please visit our <a href='https://support.leantime.io/en/article/importing-data-via-csv-1v941gy' target='_blank'>documentation</a>\"",
         "'Importe dados a partir de um arquivo CSV.'"),
    ],
    'Domain/Install/Controllers/Update.php': [
        ("'There was a problem. Please reach out to support@leantime.io for assistance.', 'error');\n                    // report",
         "'Houve um problema ao atualizar o banco de dados.', 'error');\n                    // report"),
        ("'There was a problem. Please reach out to support@leantime.io for assistance.', 'error');\n\n        return",
         "'Houve um problema ao atualizar o banco de dados. Verifique os logs da aplicação.', 'error');\n\n        return"),
    ],
    # Remetente de todos os e-mails: nome do site (LEAN_SITENAME) no lugar de "Leantime"
    'Core/Mailer.php': [
        ("""        $fromName = NameSanitizer::clean($from);
        $fromDisplay = ($fromName === '' || strcasecmp($fromName, 'Leantime') === 0)
            ? 'Leantime'
            : $fromName.' (Leantime)';""",
         """        $fromName = NameSanitizer::clean($from);
        // MAG: o nome exibido é o do site (LEAN_SITENAME); os rótulos fixos "Leantime" e
        // "Leantime System" passados pelos chamadores viram apenas o nome do site.
        $siteName = NameSanitizer::clean((string) (app('config')->sitename ?? '')) ?: 'MAG';
        $fromDisplay = ($fromName === '' || in_array(strtolower($fromName), ['leantime', 'leantime system'], true))
            ? $siteName
            : $fromName.' ('.$siteName.')';"""),
        # Cor dos e-mails enviados sem sessão (fila): vermelho MAG no lugar do azul Leantime
        ("session()->has('companysettings.primarycolor') ? '#006c9e' :", "session()->has('companysettings.primarycolor') ? '#A61915' :"),
    ],
    # Emissor do 2FA (nome que aparece no app autenticador)
    'Domain/Auth/Services/Auth.php': [
        ("new TwoFactorAuth('Leantime')", "new TwoFactorAuth('MAG')"),
    ],
    'Domain/TwoFA/Services/TwoFA.php': [
        ("new TwoFactorAuth('Leantime',", "new TwoFactorAuth('MAG',"),
    ],
    # Nome do esquema de cores padrão (Perfil → Tema)
    'Core/UI/Theme.php': [
        ("            'name' => 'Leantime',\n", "            'name' => 'MAG',\n"),
    ],
    # Webhooks (Slack, Discord, Mattermost…) e push
    'Domain/Notifications/Services/Messengers.php': [
        ("$projectName ?? 'a Leantime project'", "$projectName ?? 'um projeto'"),
        ("'username' => 'Leantime',", "'username' => 'MAG',"),
    ],
    'Domain/Notifications/Services/Push.php': [
        (": 'Leantime';", ": 'MAG';"),
    ],
    'Domain/Users/Services/Users.php': [
        ("$inviterName !== '' ? $inviterName : 'Leantime';", "$inviterName !== '' ? $inviterName : 'MAG';"),
    ],
}


def main() -> None:
    for rel, pares in TROCAS.items():
        path = APP / rel
        texto = path.read_text(encoding='utf-8')
        alterado = texto
        for antigo, novo in pares:
            n = alterado.count(antigo)
            if n == 1:
                alterado = alterado.replace(antigo, novo)
            elif n == 0 and novo in alterado:
                print(f'  já trocado: {rel}: {antigo[:50]!r}')
            else:
                raise SystemExit(f'ERRO {rel}: trecho encontrado {n} vezes: {antigo[:70]!r}')
        if alterado != texto:
            path.write_bytes(alterado.encode('utf-8'))
            print('ok', rel)


if __name__ == '__main__':
    main()


# Tours guiados (compilados no bundle JS do Leantime 3.10.0)
TROCAS_JS = {
    'public/dist/js/compiled-app.3.10.0.min.js': [
        ('different elements inside Leantime."', 'different elements of the system."'),
        ('as well as notifications and latest news about Leantime."', 'as well as notifications."'),
        ('to learn more about project management in Leantime."', 'to learn more about project management."'),
        ('the various ways to manage your tasks in Leantime."', 'the various ways to manage your tasks."'),
        ('to learn how to create and manage milestones in Leantime."', 'to learn how to create and manage milestones."'),
        ('to learn how to create and manage goals in Leantime."', 'to learn how to create and manage goals."'),
        ('are the basic building blocks in Leantime.', 'are the basic building blocks of the system.'),
    ],
}


def main_js() -> None:
    raiz = APP.parent
    for rel, pares in TROCAS_JS.items():
        path = raiz / rel
        texto = path.read_text(encoding='utf-8')
        if 'Bem-vindo ao tour do Painel' in texto:
            continue  # já traduzido por traduzir_tour.py (etapa seguinte)
        alterado = texto
        for antigo, novo in pares:
            n = alterado.count(antigo)
            if n == 1:
                alterado = alterado.replace(antigo, novo)
            elif not (n == 0 and novo in alterado):
                raise SystemExit(f'ERRO {rel}: trecho encontrado {n} vezes: {antigo[:70]!r}')
        if 'Leantime' in alterado:
            raise SystemExit(f'ERRO {rel}: ainda cita Leantime')
        if alterado != texto:
            path.write_bytes(alterado.encode('utf-8'))
            print('ok', rel)


main_js()
