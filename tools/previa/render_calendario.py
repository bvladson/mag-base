from pathlib import Path
from playwright.sync_api import sync_playwright
p = Path(__file__).parent / 'calendario.html'
with sync_playwright() as pw:
    b = pw.chromium.launch(channel='chrome', headless=True, args=['--allow-file-access-from-files'])
    for modo in ('light', 'dark'):
        pg = b.new_page(viewport={'width': 1300, 'height': 1200})
        erros = []
        pg.on('pageerror', lambda e: erros.append(str(e)[:200]))
        pg.goto(p.as_uri())
        if modo == 'dark':
            pg.evaluate("() => { const l = document.getElementById('themeStyleSheet'); l.href = l.href.replace('light.css', 'dark.css'); }")
        pg.wait_for_function('window.pronto === true', timeout=15000)
        pg.wait_for_timeout(1200)
        info = pg.evaluate("""() => ({
          cabecalho: [...document.querySelectorAll('#semana .fc-col-header-cell')].map(e => e.innerText.trim()),
          diaInteiro: document.querySelector('#semana .fc-timegrid-axis-cushion')?.innerText,
          hoje: document.querySelector('#semana .fc-today-button')?.innerText,
          horas: [...document.querySelectorAll('#semana .fc-timegrid-slot-label-cushion')].slice(8, 11).map(e => e.innerText),
          titulo: document.querySelector('#mes .fc-toolbar-title')?.innerText,
          feriados: [...document.querySelectorAll('#mes .mag-feriado')].map(e => e.innerText.trim()),
          scrollTop: document.querySelector('#semana .fc-scroller-liquid-absolute, #semana .fc-scroller')?.scrollTop
        })""")
        print(modo, erros, info)
        pg.screenshot(path=str(p.with_name(f'calendario-{modo}.png')), full_page=True)
    b.close()
