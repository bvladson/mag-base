"""Confere a tradução servida pela produção, sem login.

- Login responde 200 e todos os bundles JS do cabeçalho têm cache-bust (?v=).
- Cada bundle alterado pelo overlay: a produção serve o traduzido, o original ou outro arquivo (SHA-1).
- /api/i18n (público; é o dicionário que a tela de login usa): conta as chaves ainda com o texto em inglês
  que o pt-BR do overlay traduz, e as chaves cujo valor difere do esperado.
Grava tools/verificacao-traducao/<rótulo>.json. Uso: python verificar_traducao_publica.py antes|depois
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from inventario_ingles import OVERLAY, ORIGINAL, carregar_ini  # noqa: E402

HOST = 'task.magmoveiscorporativos.com.br'
IP = '203.0.113.10'
SITE = f'https://{HOST}'
SAIDA = TOOLS / 'verificacao-traducao'
# Chaves que o próprio serviço reescreve ao montar o dicionário (formato do usuário e fuso).
DINAMICAS = {'language.dateformat', 'language.timeformat', 'usersettings.timezone'}


def baixar(caminho: str) -> tuple[int, bytes]:
    # Corpo em arquivo: o stdout no Windows pode trocar \n por \r\n e alterar o SHA-1. Sem --compressed,
    # que o curl.exe do Windows não suporta.
    with tempfile.TemporaryDirectory() as d:
        destino = Path(d) / 'corpo'
        r = subprocess.run(['curl', '-s', '-S', '--max-time', '60', '--resolve', f'{HOST}:443:{IP}',
                            '-H', 'Accept-Language: pt-BR,pt;q=0.9', '-o', str(destino), '-w', '%{http_code}',
                            SITE + caminho], capture_output=True, check=True)
        return int(r.stdout), destino.read_bytes()


def sha1(b: bytes) -> str:
    return hashlib.sha1(b).hexdigest()


def norm(v) -> str:
    v = str(v).strip()
    if len(v) >= 2 and v[0] == v[-1] == '"':
        v = v[1:-1]
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', v.replace('\\"', '"'))).strip()


def main(rotulo: str) -> None:
    res = {}

    codigo, html = baixar('/auth/login')
    html = html.decode('utf-8', errors='replace')
    scripts = re.findall(r'src="[^"]*/dist/js/(compiled-[\w-]+\.[\d.]+\.min\.js)(\?v=[^"]*)?"', html)
    alterados = {p.name for p in (OVERLAY / 'public/dist/js').glob('*.min.js')}
    res['login'] = {'status': codigo,
                    'bundles': len(scripts),
                    'sem_cache_bust': [n for n, v in scripts if not v],
                    'alterados_sem_cache_bust': [n for n, v in scripts if not v and n in alterados],
                    'i18n_url': (re.search(r'src="[^"]*(/api/i18n[^"]*)"', html) or [None, None])[1]}

    res['bundles'] = {}
    for local in sorted((OVERLAY / 'public/dist/js').glob('*.js')):
        rel = local.relative_to(OVERLAY).as_posix()
        codigo, corpo = baixar('/' + rel.removeprefix('public/'))
        original = ORIGINAL / rel
        h = sha1(corpo)
        if h == sha1(local.read_bytes()):
            estado = 'traduzido (igual ao overlay)'
        elif original.exists() and h == sha1(original.read_bytes()):
            estado = 'original do Leantime'
        else:
            estado = 'outro'
        res['bundles'][local.name] = f'{codigo} {estado}'

    codigo, js = baixar('/api/i18n')
    m = re.search(r'dictionary:\s*(\{.*\}),\s*__:', js.decode('utf-8'), re.S)
    servido = json.loads(m.group(1)) if m else {}
    en = {**carregar_ini(ORIGINAL / 'app/Language/en-US.ini'), **carregar_ini(OVERLAY / 'custom/Language/en-US.ini')}
    pt = {**en, **carregar_ini(ORIGINAL / 'app/Language/pt-BR.ini'), **carregar_ini(OVERLAY / 'custom/Language/pt-BR.ini')}
    em_ingles = sorted(k for k in pt if k not in DINAMICAS and k in servido and k in en
                       and norm(servido[k]) == norm(en[k]) != norm(pt[k]))
    divergentes = sorted(k for k in pt if k not in DINAMICAS and k in servido and norm(servido[k]) != norm(pt[k]))
    res['i18n'] = {'status': codigo,
                   'chaves_servidas': len(servido),
                   'chaves_esperadas': len(pt),
                   'ainda_em_ingles': len(em_ingles),
                   'exemplos_em_ingles': {k: servido[k] for k in em_ingles[:8]},
                   'divergentes_do_esperado': len(divergentes),
                   'exemplos_divergentes': {k: [servido[k], norm(pt[k])] for k in divergentes[:8]}}

    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f'{rotulo}.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'resultado')
