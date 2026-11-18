"""Extrai pares (contexto, texto) de interface dos bundles JS, para montar traduções exatas.

Contexto = propriedade (label:, description:, title:, placeholder:…) ou chamada (prompt(, confirm(…).
Grava tools/inventario/js-<bundle>.tsv com: contexto<TAB>texto<TAB>ocorrências.
"""
import re
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from inventario_ingles import arquivo_efetivo  # noqa: E402

PROPS = ('label', 'description', 'title', 'placeholder', 'tooltip', 'ariaLabel', 'message', 'hint', 'emptyText',
         'buttonText', 'text', 'content', 'confirmText', 'cancelText', 'noResultsText', 'loadingText')
CHAMADAS = ('prompt', 'confirm', 'alert')
RE_PROP = re.compile(r'(?<![\w$.])(%s)\s*:\s*(["\'])((?:(?!\2)[^\\\n]){2,200}?)\2' % '|'.join(PROPS))
RE_CALL = re.compile(r'(?<![\w$])(?:window\.)?(%s)\(\s*(["\'])((?:(?!\2)[^\\\n]){2,200}?)\2' % '|'.join(CHAMADAS))
RE_ATTR = re.compile(r'["\'](aria-label|title|placeholder|data-tippy-content)["\']\s*[,:]\s*(["\'])((?:(?!\2)[^\\\n]){2,200}?)\2')


def parece_texto(t: str) -> bool:
    if not re.search(r'[A-Za-z]{2}', t):
        return False
    if re.fullmatch(r'[a-z][A-Za-z0-9]*|[a-z0-9]+(?:[-_][a-z0-9]+)+|[A-Z_]+', t):   # ids camelCase, kebab, CONSTANTES
        return False
    if re.search(r'[<>{};=]|\.(?:js|css|png|svg)\b|https?://|\bfa-', t):
        return False
    return True


def extrair(rel: str) -> Counter:
    s = arquivo_efetivo(Path(rel)).read_text(encoding='utf-8', errors='ignore')
    c = Counter()
    for rx in (RE_PROP, RE_CALL, RE_ATTR):
        for m in rx.finditer(s):
            if parece_texto(m.group(3)):
                c[(m.group(1), m.group(3))] += 1
    return c


if __name__ == '__main__':
    for rel in sys.argv[1:]:
        c = extrair(rel)
        nome = Path(rel).name.split('.')[0]
        linhas = [f'{ctx}\t{t}\t{n}' for (ctx, t), n in sorted(c.items(), key=lambda x: (x[0][0], x[0][1].lower()))]
        (TOOLS / 'inventario' / f'js-{nome}.tsv').write_text('\n'.join(linhas), encoding='utf-8')
        print(f'{nome}: {len(c)} pares')
