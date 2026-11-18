"""Regera alteracoes-vs-leantime-3.10.0.patch: diff legível do overlay contra o Leantime 3.10.0 original.

Entram PHP, Blade, INI, CSS e JS legível. Ficam de fora imagens e os bundles minificados
(*.min.js), que são alterados por tools/traduzir_js.py e não têm diff legível.
Uso: python gerar_patch.py
"""
import difflib
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
BASE = TOOLS.parent
OVERLAY = BASE / 'overlay'
ORIGINAL = Path(r'C:\Users\VLADSON\Downloads\Leantime-v3.10.0')
SAIDA = BASE / 'alteracoes-vs-leantime-3.10.0.patch'
EXTENSOES = ('.php', '.ini', '.css', '.js')


def linhas(caminho: Path):
    return caminho.read_text(encoding='utf-8').splitlines(keepends=True)


def main():
    partes = []
    arquivos = sorted(p for p in OVERLAY.rglob('*')
                      if p.is_file() and p.suffix in EXTENSOES and not p.name.endswith('.min.js'))
    for novo in arquivos:
        rel = novo.relative_to(OVERLAY).as_posix()
        antigo = ORIGINAL / rel
        a = linhas(antigo) if antigo.exists() else []
        b = linhas(novo)
        if a == b:
            continue
        de = f'leantime-3.10.0/{rel}' if antigo.exists() else '/dev/null'
        diff = list(difflib.unified_diff(a, b, de, f'mag-base/{rel}'))
        for i, linha in enumerate(diff):
            if not linha.endswith('\n'):
                diff[i] = linha + '\n\\ No newline at end of file\n'
        partes.append(''.join(diff))
    SAIDA.write_bytes(''.join(partes).encode('utf-8'))
    print(f'{len(partes)} arquivos no patch ({SAIDA.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
