"""Lista os textos dos tours guiados (Shepherd) compilados no bundle JS do Leantime."""
import json
import re
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent / 'overlay' / 'public' / 'dist' / 'js' / 'compiled-app.3.10.0.min.js'
s = BUNDLE.read_text(encoding='utf-8')

STR = r'"((?:[^"\\]|\\.)*)"'
passos = []
for m in re.finditer(r'\{id:"([^"]+)",title:' + STR + r',text:(' + STR + r'(?:\+[^,}]+?\+' + STR + r')*)', s):
    passos.append({'pos': m.start(), 'id': m.group(1), 'title': m.group(2), 'text_expr': m.group(3)})

print(f'{len(passos)} passos', file=sys.stderr)
json.dump(passos, sys.stdout, ensure_ascii=False, indent=1)
