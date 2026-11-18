"""Verifica a base MAG em produção: nenhuma marca Leantime visível e rotas removidas em 404.

Varre texto (inclusive menus ocultos, sem <script>/<style>) e atributos visíveis de cada
página, procurando "leantime", "discord.gg" e "github.com/leantime". Só lê: não cria,
altera nem envia nada (o modal de boas-vindas é escondido via CSS apenas no navegador de teste).

Uso: python verificar.py [pasta-de-saída]
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

HOST = 'task.magmoveiscorporativos.com.br'
BASE = f'https://{HOST}'
ACESSO = Path(r'C:\Users\VLADSON\Downloads\Leantime-deploy-20260928\ACESSO-LEANTIME.txt')
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / 'verificacao'
SAIDA.mkdir(parents=True, exist_ok=True)

PAGINAS = [
    ('painel', '/dashboard/home'),
    ('kanban', '/tickets/showKanban'),
    ('tabela', '/tickets/showAll'),
    ('marcos', '/tickets/roadmap'),
    ('metas', '/goalcanvas/dashboard'),
    ('meus-projetos', '/projects/showMy'),
    ('todos-projetos', '/projects/showAll'),
    ('projeto-config', '/projects/showProject/1'),
    ('perfil', '/users/editOwn'),
    ('usuarios', '/users/showAll'),
    ('empresa', '/setting/editCompanySettings'),
    ('integracoes', '/connector/show'),
    ('horas', '/timesheets/showMy'),
]

REMOVIDAS = [
    '/plugins/marketplace',
    '/plugins/myapps',
    '/plugins/details',
    '/plugins/marketplaceplugins/getLatest',
    '/notifications/news/get',
    '/notifications/news-badge/get',
    '/help/support',
    '/tiptap-test.html',
    '/dist/images/logo-powered-by-leantime.png',
]

VARREDURA = r"""() => {
  const re = /leantime|discord\.gg|github\.com\/leantime/i;
  const achados = [];
  const ignorar = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE']);
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: n => ignorar.has(n.parentNode.nodeName) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
  });
  let n;
  while ((n = walker.nextNode())) {
    if (re.test(n.nodeValue)) achados.push('texto: ' + n.nodeValue.trim().slice(0, 140));
  }
  for (const el of document.querySelectorAll('*')) {
    for (const a of ['title', 'alt', 'placeholder', 'data-tippy-content', 'aria-label', 'href', 'src']) {
      const v = el.getAttribute(a);
      if (v && re.test(v)) achados.push(`${el.tagName.toLowerCase()}[${a}]: ${v.slice(0, 140)}`);
    }
    const bg = el.getAttribute('style') || '';
    if (/leantime|images\/logo\.svg/i.test(bg)) achados.push('style: ' + bg.slice(0, 140));
  }
  if (re.test(document.title)) achados.push('title: ' + document.title);
  // Depoimentos de clientes do Leantime no login (nem todos citam o nome)
  if (document.querySelector('.socialProofContent')) achados.push('depoimentos do Leantime no login (.socialProofContent)');
  return {
    achados: [...new Set(achados)],
    titulo: document.title,
    iconesTopo: [...document.querySelectorAll('.headmenu > li i, .headmenu > li > a > span')]
      .map(e => e.className).filter(c => /fa-/.test(c)),
    logo: getComputedStyle(document.querySelector('.header .logo a') || document.body).backgroundImage,
  };
}"""

ESCONDE_MODAL = '.nyroModalBg, .nyroModalCont, .modal-backdrop, #onboardingModal { display: none !important; }'

linhas = ACESSO.read_text().splitlines()
email = next(l.split(': ', 1)[1] for l in linhas if l.startswith('Email:'))
senha = next(l.split(': ', 1)[1] for l in linhas if l.startswith('Senha temporaria:'))
resultado = {'paginas': {}, 'removidas': {}, 'erros_js': [], 'erros_http': [], 'i18n': None}

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True, args=[f'--host-resolver-rules=MAP {HOST} 203.0.113.10'])
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR')
    page = ctx.new_page()
    page.on('pageerror', lambda e: resultado['erros_js'].append(str(e)[:300]))
    page.on('response', lambda r: resultado['erros_http'].append({'url': urlsplit(r.url).path, 'status': r.status})
            if r.status >= 400 and urlsplit(r.url).path not in REMOVIDAS else None)

    def visitar(nome, caminho, esconder_modal=True, captura=True):
        resp = page.goto(BASE + caminho, wait_until='networkidle', timeout=60000)
        page.wait_for_timeout(700)
        if esconder_modal:
            page.add_style_tag(content=ESCONDE_MODAL)
        info = page.evaluate(VARREDURA)
        info['status'] = resp.status if resp else None
        info['url'] = urlsplit(page.url).path
        resultado['paginas'][nome] = info
        if captura:
            page.screenshot(path=str(SAIDA / f'{nome}.png'))

    visitar('login', '/auth/login', esconder_modal=False)
    page.locator('#username').fill(email)
    page.locator('#password').fill(senha)
    page.locator('form#login input[type=submit]').click()
    page.wait_for_url('**/dashboard/home', timeout=60000)
    page.wait_for_load_state('networkidle')

    visitar('painel-boas-vindas', '/dashboard/home', esconder_modal=False)
    for nome, caminho in PAGINAS:
        visitar(nome, caminho)

    # Menus do topo abertos (ajuda e avatar) para a captura
    page.goto(BASE + '/dashboard/home', wait_until='networkidle')
    page.add_style_tag(content=ESCONDE_MODAL)
    page.locator('.headmenu .fa-question-circle').first.click()
    page.wait_for_timeout(400)
    page.screenshot(path=str(SAIDA / 'menu-ajuda.png'))

    for caminho in REMOVIDAS:
        r = page.request.get(BASE + caminho, max_redirects=0)
        resultado['removidas'][caminho] = r.status

    # Tour guiado: o bundle realmente servido (com o cache-bust da página) precisa estar em português
    page.goto(BASE + '/dashboard/home', wait_until='networkidle')
    src_app = page.locator('script[src*="compiled-app"]').first.get_attribute('src')
    bundle = page.request.get(src_app).text()
    resultado['tour'] = {
        'src': urlsplit(src_app).path + '?' + urlsplit(src_app).query,
        'portugues': 'Bem-vindo ao tour do Painel' in bundle and 'Atualizações rápidas de status' in bundle,
        'ingles_restante': [t for t in ('Welcome to the Dashboard Tour', 'Quick Status Updates', 'Your Kanban Board',
                                        'Congratulations!', 'Objectives & Metrics') if t in bundle],
    }
    resultado['css_tema'] = [link.get_attribute('href') for link in page.locator('link[href*="/theme/"]').all()]

    # Dicionário de textos do JS: só os valores contam (há chaves como "#Leantime 2.3.16",
    # que são linhas de comentário do .ini lidas como chave vazia e nunca aparecem na tela)
    i18n = page.request.get(BASE + '/api/i18n').text()
    pares = re.findall(r'"((?:[^"\\]|\\.)*)":"((?:[^"\\]|\\.)*)"', i18n)
    resultado['i18n'] = sorted(f'{k} = {v[:100]}' for k, v in pares if re.search(r'leantime', v, re.I))

    page.goto(BASE + '/auth/logout', wait_until='networkidle')
    browser.close()

(SAIDA / 'resultado.json').write_text(json.dumps(resultado, indent=2, ensure_ascii=False), encoding='utf-8')

falhas = []
for nome, info in resultado['paginas'].items():
    if info['status'] != 200:
        falhas.append(f'{nome}: HTTP {info["status"]}')
    for a in info['achados']:
        falhas.append(f'{nome}: {a}')
    if any(re.search('puzzle|bolt', c) for c in info['iconesTopo']):
        falhas.append(f'{nome}: ícone de apps/novidades no topo {info["iconesTopo"]}')
for caminho, status in resultado['removidas'].items():
    if status != 404:
        falhas.append(f'rota removida respondeu {status}: {caminho}')
falhas += [f'i18n: {t}' for t in resultado['i18n']]
if not resultado['tour']['portugues'] or resultado['tour']['ingles_restante']:
    falhas.append(f'tour: {resultado["tour"]}')
for href in resultado['css_tema']:
    if '.min.css' in href or not re.search(r'\?v=\d{9,}$', href):
        falhas.append(f'CSS do tema sem cache-bust por data: {href}')
falhas += [f'erro JS: {e}' for e in resultado['erros_js']]
falhas += [f'HTTP {e["status"]}: {e["url"]}' for e in resultado['erros_http']]

print(f'páginas: {len(resultado["paginas"])}  rotas removidas: {resultado["removidas"]}')
print('\n'.join(falhas) if falhas else 'OK: nenhuma marca Leantime encontrada e rotas removidas em 404')
sys.exit(1 if falhas else 0)
