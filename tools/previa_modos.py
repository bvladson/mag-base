"""Capturas dos modos claro, escuro e sistema, sem alterar preferências da conta.

- Login (sem sessão): o modo vem do cookie colorMode; "system" é testado emulando o
  sistema operacional claro e escuro.
- Páginas logadas: capturadas como o servidor entrega (modo salvo na conta) e com a folha
  trocada no navegador de teste (o mesmo que a prévia do perfil faz), sem gravar nada.
- O tour do painel do projeto é iniciado só no navegador, para conferir o 1º passo.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HOST = 'task.magmoveiscorporativos.com.br'
BASE = f'https://{HOST}'
ACESSO = Path(r'C:\Users\VLADSON\Downloads\Leantime-deploy-20260928\ACESSO-LEANTIME.txt')
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / 'previa-modos'
SAIDA.mkdir(parents=True, exist_ok=True)
ESCONDE_MODAL = '.nyroModalBg, .nyroModalCont, .modal-backdrop, #onboardingModal { display: none !important; }'
TROCA_FOLHA = """(modo) => {
  document.getElementById('themeStyleSheetDark')?.remove();
  const l = document.getElementById('themeStyleSheet');
  const novo = l.href.replace(/(light|dark)\\.css/, modo + '.css');
  if (novo === l.href) return true;           // já está no modo pedido: não há carga a esperar
  return new Promise(r => {
    l.addEventListener('load', () => r(true), {once: true});
    setTimeout(() => r(false), 8000);
    l.href = novo;
  });
}"""
INFO = """() => ({
  folhas: [...document.querySelectorAll('link[href*="/theme/"]')].map(l => ({href: l.getAttribute('href').replace(/^https:\\/\\/[^/]+/, ''), media: l.media})),
  colorScheme: document.querySelector('meta[name=color-scheme]')?.content,
  fundo: getComputedStyle(document.body).backgroundColor,
  bgPage: getComputedStyle(document.documentElement).getPropertyValue('--bg-page').trim(),
})"""

linhas = ACESSO.read_text().splitlines()
email = next(l.split(': ', 1)[1] for l in linhas if l.startswith('Email:'))
senha = next(l.split(': ', 1)[1] for l in linhas if l.startswith('Senha temporaria:'))
res = {}

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True, args=[f'--host-resolver-rules=MAP {HOST} 203.0.113.10'])

    # 1) Login nos três modos (cookie) — "system" com o sistema operacional claro e escuro
    for modo, so in [('light', 'light'), ('dark', 'dark'), ('system', 'light'), ('system', 'dark')]:
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', color_scheme=so)
        ctx.add_cookies([{'name': 'colorMode', 'value': modo, 'domain': HOST, 'path': '/', 'secure': True}])
        pg = ctx.new_page()
        pg.goto(BASE + '/auth/login', wait_until='networkidle')
        nome = f'login-{modo}' + (f'-so-{so}' if modo == 'system' else '')
        res[nome] = pg.evaluate(INFO)
        pg.screenshot(path=str(SAIDA / f'{nome}.png'))
        ctx.close()

    # 2) Páginas logadas: como servidas e com a outra folha aplicada só no navegador
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR')
    pg = ctx.new_page()
    pg.goto(BASE + '/auth/login', wait_until='networkidle')
    pg.locator('#username').fill(email)
    pg.locator('#password').fill(senha)
    pg.locator('form#login input[type=submit]').click()
    pg.wait_for_url('**/dashboard/home', timeout=60000)

    for nome, caminho in [('painel', '/dashboard/home'), ('kanban', '/tickets/showKanban'),
                          ('projeto', '/dashboard/show'), ('perfil-tema', '/users/editOwn#theme')]:
        for modo in ('dark', 'light'):
            pg.goto(BASE + caminho, wait_until='networkidle')
            pg.add_style_tag(content=ESCONDE_MODAL)
            pg.evaluate(TROCA_FOLHA, modo)
            pg.wait_for_timeout(500)
            if nome == 'perfil-tema':
                pg.locator('a[href="#theme"]').first.click()
                pg.wait_for_timeout(500)
            res[f'{nome}-{modo}'] = pg.evaluate(INFO)
            pg.screenshot(path=str(SAIDA / f'{nome}-{modo}.png'))

    # 3) Tour do painel do projeto: 1º passo de "Atualizações rápidas de status"
    for modo in ('dark', 'light'):
        pg.goto(BASE + '/dashboard/show', wait_until='networkidle')
        pg.add_style_tag(content=ESCONDE_MODAL)
        pg.evaluate(TROCA_FOLHA, modo)
        pg.evaluate('() => leantime.helperController.startProjectDashboardTour()')
        pg.wait_for_timeout(900)
        for _ in range(3):  # avança até "Atualizações rápidas de status" (4º passo)
            pg.locator('.shepherd-element:visible .shepherd-button').last.click()
            pg.wait_for_timeout(600)
        res[f'tour-{modo}'] = pg.locator('.shepherd-element:visible').inner_text()
        pg.screenshot(path=str(SAIDA / f'tour-{modo}.png'))

    pg.goto(BASE + '/auth/logout', wait_until='networkidle')
    browser.close()

(SAIDA / 'resultado.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
print(json.dumps(res, indent=1, ensure_ascii=False))
