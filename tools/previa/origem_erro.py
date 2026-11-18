from pathlib import Path
from playwright.sync_api import sync_playwright
p = Path(__file__).parent / 'calendario-widget.html'
with sync_playwright() as pw:
    b = pw.chromium.launch(channel='chrome', headless=True, args=['--allow-file-access-from-files'])
    pg = b.new_page()
    pg.on('pageerror', lambda e: print('ERRO:', e.message, '\n', (e.stack or '')[:500]))
    pg.goto(p.as_uri()); pg.wait_for_timeout(3000)
    # Mesmo cenário sem o mag-calendario.js, para comparar
    s = p.read_text(encoding='utf-8').replace('<script defer src="../../overlay/public/dist/js/mag-calendario.js"></script>', '')
    q = p.with_name('calendario-widget-sem-mag.html'); q.write_text(s, encoding='utf-8')
    print('--- sem o script MAG ---')
    pg.goto(q.as_uri()); pg.wait_for_timeout(3000)
    print('cabecalho sem MAG:', pg.evaluate("() => [...document.querySelectorAll('.fc-col-header-cell')].map(e => e.innerText.trim()).slice(0,2)"),
          pg.evaluate("() => document.querySelector('.fc-timegrid-axis-cushion')?.innerText"))
    b.close()
