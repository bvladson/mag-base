"""Lista literais de string com cara de frase em inglês num bundle JS (revisão manual)."""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from inventario_ingles import arquivo_efetivo, eh_ingles  # noqa: E402

s = arquivo_efetivo(Path(sys.argv[1])).read_text(encoding='utf-8', errors='ignore')
vistos = set()
for m in re.finditer(r'(["\'])((?:(?!\1)[^\\n]){3,200}?)\1', s):
    t = m.group(2)
    if t in vistos or not re.search(r'[A-Za-z]{3}', t) or re.search(r'[{}<>;=]|https?:|\.(js|css|php)\b', t):
        continue
    if re.fullmatch(r'[\w.\-#/:\[\]()*, ]+', t) and ' ' not in t.strip():
        continue
    if eh_ingles(t):
        vistos.add(t)
        print(repr(t), '|', s[max(0, m.start() - 45):m.start()].replace('\n', ' ')[-45:])
