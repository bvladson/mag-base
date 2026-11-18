from pathlib import Path
from playwright.sync_api import sync_playwright
p = Path(__file__).parent / 'calendario-widget.html'
with sync_playwright() as pw:
    b = pw.chromium.launch(channel='chrome', headless=True, args=['--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1300, 'height': 700})
    erros = []
    pg.on('pageerror', lambda e: erros.append(str(e)[:160]))
    pg.goto(p.as_uri())
    pg.wait_for_function('window.resultado !== undefined', timeout=20000)
    pg.wait_for_timeout(1500)
    print('resultado:', pg.evaluate('window.resultado'))
    print('erros de pagina:', erros[:6])
    print(pg.evaluate(r"""() => ({
      fullcalendarEnvolvido: !!window.magCalendario,
      cabecalho: [...document.querySelectorAll('.fc-col-header-cell')].map(e => e.innerText.replace(/\n/g,' ').trim()),
      diaInteiro: document.querySelector('.fc-timegrid-axis-cushion')?.innerText,
      horas: [...document.querySelectorAll('.fc-timegrid-slot-label-cushion')].slice(8, 10).map(e => e.innerText),
      eventos: [...document.querySelectorAll('.fc-event')].map(e => e.className.split(' ').filter(c => c.startsWith('mag-')).join(',') + ' | ' + e.innerText.replace(/\n/g,' ').slice(0, 50)),
    })"""))
    pg.screenshot(path=str(p.with_name('calendario-widget.png')))
    b.close()
