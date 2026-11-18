"""Lista textos de interface em inglês nos bundles JS (editor, app, upload, tour).

Procura valores de propriedades/argumentos que viram texto na tela: title, description,
placeholder, label, tooltip, aria-label, message, text, html, confirm/alert, setAttribute("title").
Uso: python listar_js.py <bundle> [<bundle>...]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inventario_ingles import arquivo_efetivo, eh_ingles, parece_codigo  # noqa: E402

PADRAO = re.compile(
    r"""(?:\b(title|description|placeholder|label|tooltip|ariaLabel|message|text|html|hint|emptyText|buttonText|name)\s*:\s*"""
    r"""|\b(confirm|alert|html|text|append|prepend)\s*\(\s*"""
    r"""|setAttribute\(\s*["'](?:title|aria-label|placeholder|data-tippy-content)["']\s*,\s*"""
    r"""|["'](?:aria-label|data-tippy-content|title|placeholder)["']\s*:\s*)"""
    r"""(["'`])((?:(?!\3)[^\\\n]){2,160}?)\3""")


def listar(rel: str):
    s = arquivo_efetivo(Path(rel)).read_text(encoding='utf-8', errors='ignore')
    vistos = []
    for m in PADRAO.finditer(s):
        t = m.group(4)
        if t in vistos or parece_codigo(t) or t.startswith(('fa ', 'fas ', 'far ', 'fab ', 'fa-')):
            continue
        if re.search(r'[A-Za-z]', t) and eh_ingles(t):
            vistos.append(t)
    return vistos


if __name__ == '__main__':
    for rel in sys.argv[1:]:
        itens = listar(rel)
        print(f'== {rel} ({len(itens)})')
        for t in itens:
            print('  ', t)
