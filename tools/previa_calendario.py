"""Captura o calendário pessoal e o widget do painel (somente leitura)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
HOST = 'task.magmoveiscorporativos.com.br'; BASE = f'https://{HOST}'
ACESSO = Path(r'C:\Users\VLADSON\Downloads\Leantime-deploy-20260928\ACESSO-LEANTIME.txt')
SAIDA = Path(__file__).parent / 'previa-calendario'; SAIDA.mkdir(exist_ok=True)
l = ACESSO.read_text().splitlines()
email = next(x.split(': ', 1)[1] for x in l if x.startswith('Email:'))
senha = next(x.split(': ', 1)[1] for x in l if x.startswith('Senha temporaria:'))
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True, args=[f'--host-resolver-rules=MAP {HOST} 203.0.113.10'])
    pg = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR').new_page()
    pg.goto(BASE + '/auth/login', wait_until='networkidle')
    pg.locator('#username').fill(email); pg.locator('#password').fill(senha)
    pg.locator('form#login input[type=submit]').click(); pg.wait_for_url('**/dashboard/home', timeout=60000)
    pg.goto(BASE + '/calendar/showMyCalendar', wait_until='networkidle'); pg.wait_for_timeout(1500)
    pg.add_style_tag(content='.nyroModalBg,.nyroModalCont,.modal-backdrop{display:none!important}')
    pg.screenshot(path=str(SAIDA / 'calendario-pessoal.png'))
    print(pg.evaluate("() => [...document.querySelectorAll('.fc-col-header-cell, .fc-timegrid-axis, .fc-timegrid-slot-label')].slice(0,12).map(e => e.innerText.trim()).filter(Boolean)"))
    pg.goto(BASE + '/auth/logout', wait_until='networkidle'); b.close()
