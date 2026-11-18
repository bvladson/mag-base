from pathlib import Path
from playwright.sync_api import sync_playwright
HOST = 'task.magmoveiscorporativos.com.br'; BASE = f'https://{HOST}'
l = Path(r'C:\Users\VLADSON\Downloads\Leantime-deploy-20260928\ACESSO-LEANTIME.txt').read_text().splitlines()
email = next(x.split(': ', 1)[1] for x in l if x.startswith('Email:'))
senha = next(x.split(': ', 1)[1] for x in l if x.startswith('Senha temporaria:'))
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True, args=[f'--host-resolver-rules=MAP {HOST} 203.0.113.10'])
    pg = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR').new_page()
    pg.goto(BASE + '/auth/login', wait_until='networkidle')
    pg.locator('#username').fill(email); pg.locator('#password').fill(senha)
    pg.locator('form#login input[type=submit]').click()
    pg.wait_for_timeout(6000)
    print('url:', pg.url)
    print('mensagens:', pg.evaluate("() => [...document.querySelectorAll('.alert, .growl, .notification, .inputwrapper .error, .regpanelinner p, .jGrowl-message')].map(e => e.innerText.trim()).filter(Boolean).slice(0,5)"))
    pg.screenshot(path=str(Path(__file__).parent / 'previa-calendario' / 'diag-login.png'))
    b.close()
