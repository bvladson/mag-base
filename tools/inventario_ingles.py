"""Inventário de textos em inglês visíveis no sistema (base MAG sobre Leantime 3.10.0).

Fontes:
  1. chaves de idioma sem tradução pt-BR (caem no en-US) ou com valor igual ao inglês;
  2. textos fixos nos templates Blade (nós de texto e atributos visíveis);
Considera o overlay da base MAG por cima do Leantime original.

Uso: python inventario_ingles.py  → grava tools/inventario/*.json e imprime o resumo.
"""
import json
import re
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
BASE = TOOLS.parent
ORIGINAL = Path(r'C:\Users\VLADSON\Downloads\Leantime-v3.10.0')
OVERLAY = BASE / 'overlay'
SAIDA = TOOLS / 'inventario'

# Palavras que só existem em inglês (evita "no", "a", "do", "as", "me"... que também são português)
INGLES = set('''
the your you yours this that these those with without from into onto about above below after before while
what who whom which when where why how here there then than also only just still yet ever never always
is are was were be been being has have had having do does did done doing can could will would shall should may might must
please click drag drop enter type press choose pick select selected searching search filter filters sort sorted group grouped
add added adding create created creating new edit edited editing delete deleted deleting remove removed removing
save saved saving cancel close closed open opened show showing hide hidden view views viewing back next previous prev
all none any some every each other more less most least many much few first last latest recent recently
name names title description details detail date dates start started starting end ended ending due deadline
goal goals task tasks project projects milestone milestones board boards track tracking tracked risk progress
settings setting user users team teams member members comment comments file files upload uploaded download
import export report reports time hours hour minutes minute day days week weeks month months year years
today tomorrow yesterday now soon later overdue upcoming schedule scheduled
yes not no-one nothing something anything everything someone anyone everyone
and or but if because so for of to by on off in out at up down over under between
help learn more read about get got make made use used using need needs want like see seen find found
success successfully error failed failure warning invalid required optional unknown loading please
my our their his her its we they them us me i'm you're it's don't can't won't isn't aren't doesn't
owner admin manager editor reader client clients company account accounts profile password email
list lists table tables card cards column columns row rows item items field fields value values
number numbers text title summary overview dashboard home status priority type types tag tags
week's today's there's that's here's what's let's
'''.split())
PORTUGUES = set('''
de da do das dos para com sem uma um umas uns que não sim seu sua seus suas nosso nossa este esta esse essa isso
novo nova criar editar excluir salvar cancelar fechar abrir mostrar tarefa tarefas projeto projetos meta metas
data início fim prazo equipe usuário usuários arquivo arquivos relatório relatórios hora horas dia dias semana mês ano
'''.split())

ATRIBUTOS = ('placeholder', 'title', 'alt', 'aria-label', 'data-tippy-content', 'label', 'labelText', 'headline',
             'text', 'helpText', 'caption', 'emptyText', 'tooltip', 'value', 'data-placeholder', 'subtitle')


def _vocabulario(arquivo: Path) -> set:
    texto = re.sub(r'<[^>]+>', ' ', arquivo.read_text(encoding='utf-8', errors='ignore'))
    valores = ' '.join(re.findall(r'=\s*"(.*)"', texto))
    return {p.lower() for p in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ']+", valores)}


# Vocabulário dos próprios arquivos de idioma: palavra exclusiva do en-US conta como inglês,
# exclusiva do pt-BR como português; as comuns (Status, Sprint, Kanban…) não contam.
_EN = _vocabulario(ORIGINAL / 'app/Language/en-US.ini')
_PT = _vocabulario(ORIGINAL / 'app/Language/pt-BR.ini')
INGLES |= (_EN - _PT)
PORTUGUES |= (_PT - _EN) - INGLES


def eh_ingles(texto: str) -> bool:
    palavras = re.findall(r"[A-Za-z][A-Za-z']+", texto)
    if not palavras:
        return False
    if re.search(r'[áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]', texto):
        return False
    minusculas = [p.lower() for p in palavras]
    ingles = sum(p in INGLES for p in minusculas)
    portugues = sum(p in PORTUGUES for p in minusculas)
    return ingles > 0 and ingles >= portugues


def arquivo_efetivo(rel: Path) -> Path:
    sobre = OVERLAY / rel
    return sobre if sobre.exists() else ORIGINAL / rel


def remover_diretivas(s: str) -> str:
    """Remove @diretiva(...) com parênteses balanceados e @diretivas sem argumento."""
    saida, i = [], 0
    while i < len(s):
        m = re.compile(r'@[A-Za-z_]\w*').search(s, i)
        if not m:
            saida.append(s[i:])
            break
        saida.append(s[i:m.start()])
        j = m.end()
        k = j
        while k < len(s) and s[k] in ' \t':
            k += 1
        if k < len(s) and s[k] == '(':
            nivel, k2 = 0, k
            while k2 < len(s):
                if s[k2] == '(':
                    nivel += 1
                elif s[k2] == ')':
                    nivel -= 1
                    if nivel == 0:
                        break
                k2 += 1
            j = k2 + 1
        saida.append(' ')
        i = j
    return ''.join(saida)


def limpar_blade(s: str) -> str:
    s = re.sub(r'\{\{--.*?--\}\}', ' ', s, flags=re.S)
    s = re.sub(r'@php.*?@endphp', ' ', s, flags=re.S)
    s = re.sub(r'<script\b.*?</script>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<style\b.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<\?php.*?\?>', ' ', s, flags=re.S)
    s = re.sub(r'\{\{.*?\}\}|\{!!.*?!!\}', ' ', s, flags=re.S)
    return remover_diretivas(s)


def parece_codigo(t: str) -> bool:
    return bool(re.search(r'\$|::|->|=>|\(\)|\[|\]|;|\bescape\(', t))


def textos_do_template(conteudo: str):
    s = limpar_blade(conteudo)
    achados = []
    # Nós de texto (entre tags), sem expressões Blade
    for m in re.finditer(r'>([^<>]+)<', s):
        t = re.sub(r'\s+', ' ', m.group(1)).strip()
        if t and not parece_codigo(t) and eh_ingles(t):
            achados.append(('texto', t))
    # Atributos visíveis com valor literal (sem expressão)
    for m in re.finditer(r'(?<![:\w-])(%s)\s*=\s*"([^"{}$]*[A-Za-z][^"{}$]*)"' % '|'.join(map(re.escape, ATRIBUTOS)), s):
        t = m.group(2).strip()
        if eh_ingles(t) and not re.fullmatch(r'[\w.\-/#]+', t):
            achados.append((m.group(1), t))
    return achados


PHP_MENSAGEM = re.compile(
    r"""(setNotification|displayNotification|growl|'message'\s*=>|"message"\s*=>|throw new \w*Exception|abort\(\d+,)"""
    r"""\s*\(?\s*(['"])((?:(?!\2).){6,}?)\2""")

JS_MENSAGEM = re.compile(
    r"""(message|title|text|placeholder|confirm|alert|html|label|tooltip|content)\s*[:(]\s*(["'])((?:(?!\2)[^\\\n]){4,}?)\2""")


def mensagens_php() -> dict:
    achados = {}
    for f in sorted((ORIGINAL / 'app').rglob('*.php')):
        if f.name.endswith('.blade.php') or 'Language' in f.parts:
            continue
        rel = f.relative_to(ORIGINAL)
        s = arquivo_efetivo(rel).read_text(encoding='utf-8', errors='ignore')
        for m in PHP_MENSAGEM.finditer(s):
            t = m.group(3)
            if eh_ingles(t) and not parece_codigo(t):
                achados.setdefault(str(rel).replace('\\', '/'), []).append((m.group(1), t))
    return achados


def mensagens_js() -> dict:
    achados = {}
    for f in sorted((ORIGINAL / 'public/dist/js').glob('compiled-*.js')):
        if 'tiptap-tests' in f.name:
            continue
        rel = f.relative_to(ORIGINAL)
        s = arquivo_efetivo(rel).read_text(encoding='utf-8', errors='ignore')
        vistos = set()
        for m in JS_MENSAGEM.finditer(s):
            t = m.group(3)
            if t in vistos or parece_codigo(t) or not re.search(r'[a-z] [a-zA-Z]', t):
                continue
            if eh_ingles(t):
                vistos.add(t)
                achados.setdefault(f.name, []).append((m.group(1), t))
    return achados


def carregar_ini(f: Path) -> dict:
    d = {}
    if f.exists():
        for linha in f.read_text(encoding='utf-8').splitlines():
            m = re.match(r'^\s*([^;#=\s][^=]*?)\s*=\s*(.*)$', linha)
            if m:
                d[m.group(1)] = m.group(2).strip()
    return d


def main() -> None:
    SAIDA.mkdir(exist_ok=True)
    en = carregar_ini(ORIGINAL / 'app/Language/en-US.ini')
    pt = carregar_ini(ORIGINAL / 'app/Language/pt-BR.ini')
    cu = carregar_ini(OVERLAY / 'custom/Language/pt-BR.ini')

    def txt(v):
        return re.sub(r'<[^>]+>', '', v.strip().strip('"')).strip()

    faltando = {k: v for k, v in en.items() if k not in pt and k not in cu and txt(v)}
    iguais = {k: v for k, v in en.items() if k in pt and k not in cu and txt(pt[k]) == txt(v) and eh_ingles(txt(v))}

    templates = {}
    for f in sorted((ORIGINAL / 'app').rglob('*.blade.php')):
        rel = f.relative_to(ORIGINAL)
        conteudo = arquivo_efetivo(rel).read_text(encoding='utf-8', errors='ignore')
        achados = textos_do_template(conteudo)
        if achados:
            templates[str(rel).replace('\\', '/')] = achados

    (SAIDA / 'chaves-faltando.json').write_text(json.dumps(faltando, indent=1, ensure_ascii=False), encoding='utf-8')
    (SAIDA / 'chaves-iguais.json').write_text(json.dumps(iguais, indent=1, ensure_ascii=False), encoding='utf-8')
    (SAIDA / 'templates.json').write_text(json.dumps(templates, indent=1, ensure_ascii=False), encoding='utf-8')

    php = mensagens_php()
    js = mensagens_js()
    (SAIDA / 'php.json').write_text(json.dumps(php, indent=1, ensure_ascii=False), encoding='utf-8')
    (SAIDA / 'js.json').write_text(json.dumps(js, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'PHP: {sum(len(v) for v in php.values())} mensagens em {len(php)} arquivos')
    print('JS:', {k: len(v) for k, v in js.items()})

    total = sum(len(v) for v in templates.values())
    print(f'chaves sem tradução: {len(faltando)} | chaves iguais ao inglês: {len(iguais)}')
    print(f'templates com texto fixo em inglês: {len(templates)} arquivos, {total} textos')
    por_dominio = {}
    for rel, achados in templates.items():
        partes = rel.split('/')
        dom = partes[2] if partes[1] == 'Domain' else partes[1]
        por_dominio[dom] = por_dominio.get(dom, 0) + len(achados)
    print('por área:', sorted(por_dominio.items(), key=lambda x: -x[1]))


if __name__ == '__main__':
    main()
