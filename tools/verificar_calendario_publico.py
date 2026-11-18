"""Verifica o calendário com os arquivos servidos pela produção, sem login e sem gravar nada."""
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
HOST = 'task.magmoveiscorporativos.com.br'; BASE = f'https://{HOST}'
SAIDA = Path(__file__).parent / 'verificacao-calendario'; SAIDA.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True, args=[f'--host-resolver-rules=MAP {HOST} 203.0.113.10'])
    pg = b.new_context(viewport={'width': 1300, 'height': 900}, locale='pt-BR').new_page()
    erros, falhas = [], []
    pg.on('pageerror', lambda e: erros.append(str(e)[:200]))
    pg.on('response', lambda r: falhas.append((urlsplit(r.url).path, r.status)) if r.status >= 400 else None)
    pg.goto(BASE + '/auth/login', wait_until='networkidle')
    info = pg.evaluate(r"""() => ({
      script: document.querySelector('script[src*="mag-calendario.js"]')?.getAttribute('src').replace(/^https:\/\/[^/]+/, ''),
      envolvido: !!window.magCalendario,
      locales: FullCalendar.globalLocales.map(l => l.code),
      horaIdioma: leantime.i18n.__('language.timeformat'),
      primeiroDia: leantime.i18n.__('language.firstDayOfWeek'),
    })""")
    print(info)
    # Calendário temporário, só neste navegador, com as opções que o sistema usa
    pg.evaluate(r"""() => {
      document.body.innerHTML = '<div style="padding:16px;background:var(--bg-page)"><div id="c1" style="height:520px;background:var(--bg-surface)"></div><div id="c2" style="height:520px;margin-top:16px;background:var(--bg-surface)"></div></div>';
      const base = {timeZone: leantime.i18n.__('usersettings.timezone'), firstDay: leantime.i18n.__('language.firstDayOfWeek'),
        eventTimeFormat: leantime.dateHelper.getFormatFromSettings('timeformat', 'luxon'),
        slotLabelFormat: leantime.dateHelper.getFormatFromSettings('timeformat', 'luxon'), headerToolbar: {left: 'title', right: 'today prev,next'}, height: 520};
      new FullCalendar.Calendar(document.getElementById('c1'), Object.assign({}, base, {initialView: 'timeGridWeek', initialDate: '2027-02-08'})).render();
      new FullCalendar.Calendar(document.getElementById('c2'), Object.assign({}, base, {initialView: 'dayGridMonth', initialDate: '2026-11-10'})).render();
    }""")
    pg.wait_for_timeout(1500)
    print(pg.evaluate(r"""() => ({
      semana: [...document.querySelectorAll('#c1 .fc-col-header-cell')].map(e => e.innerText.replace(/\n/g, ' ').trim()),
      diaInteiro: document.querySelector('#c1 .fc-timegrid-axis-cushion')?.innerText,
      horas: [...document.querySelectorAll('#c1 .fc-timegrid-slot-label-cushion')].slice(13, 15).map(e => e.innerText),
      feriadosSemana: [...document.querySelectorAll('#c1 .mag-feriado')].map(e => e.innerText.trim()),
      tituloMes: document.querySelector('#c2 .fc-toolbar-title')?.innerText,
      feriadosMes: [...document.querySelectorAll('#c2 .mag-feriado')].map(e => e.innerText.trim()),
    })"""))
    pg.screenshot(path=str(SAIDA / 'calendario-producao.png'), full_page=True)
    print('erros JS:', erros, '| HTTP >= 400:', falhas)
    b.close()
