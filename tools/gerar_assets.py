"""Gera logos e ícones MAG para a base, a partir do logo oficial usado no BIomie.

Fonte: biomie/images/logo-mag.png ("Grupo MAG Móveis Corporativos", vermelho e preto).
Saída: overlay/public/dist/images/mag/* (URLs novas, fora do cache de 7 dias de /dist/)
e substitutos dos arquivos antigos do Leantime nos mesmos nomes (logo.svg, favicon…),
para qualquer referência que tenha sobrado.
"""
import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw

BASE = Path(__file__).resolve().parent.parent
FONTE = Path(r'C:\Users\VLADSON\Downloads\biomie\images\logo-mag.png')
IMAGES = BASE / 'overlay' / 'public' / 'dist' / 'images'
MAG_DIR = IMAGES / 'mag'
PUBLIC = BASE / 'overlay' / 'public'

VERMELHO = (152, 7, 7)          # #980707
VINHO = (36, 11, 11)            # #240B0B
FUNDO = (255, 247, 245)         # #FFF7F5
BORDA = (233, 222, 220)         # #E9DEDC
TEXTO_CLARO = (233, 222, 220)   # "Grupo" / "MÓVEIS CORPORATIVOS" sobre fundo escuro


def eh_vermelho(p):
    return p[3] > 0 and p[0] > 90 and p[0] > 2 * p[1]


def recolorir(im, cor_mag, cor_texto):
    """Mantém o alfa e troca a cor: bloco MAG (vermelho) e textos (preto)."""
    out = Image.new('RGBA', im.size)
    src, dst = im.load(), out.load()
    for y in range(im.height):
        for x in range(im.width):
            p = src[x, y]
            if p[3] == 0:
                continue
            cor = cor_mag if eh_vermelho(p) else cor_texto
            dst[x, y] = (*cor, p[3])
    return out


def bbox_vermelho(im):
    mask = Image.new('L', im.size)
    src, m = im.load(), mask.load()
    for y in range(im.height):
        for x in range(im.width):
            if eh_vermelho(src[x, y]) and src[x, y][3] > 40:
                m[x, y] = 255
    return mask.getbbox()


def svg_com_png(im, titulo):
    buf = io.BytesIO()
    im.save(buf, 'PNG', optimize=True)
    dados = base64.b64encode(buf.getvalue()).decode('ascii')
    w, h = im.size
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'<title>{titulo}</title>'
            f'<image width="{w}" height="{h}" href="data:image/png;base64,{dados}"/></svg>\n')


def icone(tamanho, marca, arredondado=True):
    """Quadrado #980707 com o bloco MAG branco centralizado."""
    escala = 4  # desenha maior e reduz, para bordas suaves
    t = tamanho * escala
    fundo = Image.new('RGBA', (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(fundo)
    raio = int(t * 0.22) if arredondado else 0
    d.rounded_rectangle([0, 0, t - 1, t - 1], radius=raio, fill=(*VERMELHO, 255))
    largura = int(t * 0.74)
    altura = int(marca.height * largura / marca.width)
    m = marca.resize((largura, altura), Image.LANCZOS)
    fundo.alpha_composite(m, ((t - largura) // 2, (t - altura) // 2))
    return fundo.resize((tamanho, tamanho), Image.LANCZOS)


def miniatura_tema(w=1712, h=897):
    """Prévia do tema MAG para a escolha de tema no perfil (Perfil → Tema)."""
    im = Image.new('RGB', (w, h), FUNDO)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 60], fill=VINHO)                                     # cabeçalho
    d.rounded_rectangle([14, 80, 290, h - 14], radius=28, fill=VINHO)          # menu lateral
    d.rounded_rectangle([34, 100, 270, 146], radius=18, fill=(70, 20, 20))     # item ativo
    for i in range(4):                                                         # itens do menu
        d.rounded_rectangle([50, 170 + i * 50, 230, 186 + i * 50], radius=8, fill=(90, 60, 58))
    for i in range(4):                                                         # cards de indicador
        x = 316 + i * 346
        d.rounded_rectangle([x, 84, x + 330, 200], radius=18, fill=(255, 255, 255), outline=BORDA, width=2)
    d.rounded_rectangle([316, 224, 1180, h - 14], radius=22, fill=(255, 255, 255), outline=BORDA, width=2)
    d.rounded_rectangle([1204, 224, w - 18, h - 14], radius=22, fill=(255, 255, 255), outline=BORDA, width=2)
    d.rounded_rectangle([1240, 260, 1320, 300], radius=12, fill=VERMELHO)
    d.rounded_rectangle([1000, 250, 1150, 290], radius=20, fill=VERMELHO)      # botão principal
    return im


def main():
    MAG_DIR.mkdir(parents=True, exist_ok=True)
    original = Image.open(FONTE).convert('RGBA')

    claro = recolorir(original, (255, 255, 255), TEXTO_CLARO)
    x0, y0, x1, y1 = bbox_vermelho(original)
    marca_branca = claro.crop((x0, y0, x1 + 1, y1 + 1))

    # Logos
    (MAG_DIR / 'logo-cabecalho.svg').write_text(svg_com_png(marca_branca, 'MAG'), encoding='utf-8')
    (MAG_DIR / 'logo-login.svg').write_text(svg_com_png(claro, 'Grupo MAG Móveis Corporativos'), encoding='utf-8')
    (MAG_DIR / 'logo-cor.svg').write_text(svg_com_png(original, 'Grupo MAG Móveis Corporativos'), encoding='utf-8')
    original.save(MAG_DIR / 'logo-cor.png', optimize=True)

    # Ícones
    icone(64, marca_branca).save(MAG_DIR / 'favicon.png', optimize=True)
    icone(180, marca_branca, arredondado=False).save(MAG_DIR / 'apple-touch-icon.png', optimize=True)
    icone(192, marca_branca).save(MAG_DIR / 'icon-192.png', optimize=True)
    icone(512, marca_branca).save(MAG_DIR / 'icon-512.png', optimize=True)

    # Substitutos dos arquivos do Leantime (mesmos nomes)
    (IMAGES / 'logo.svg').write_text(svg_com_png(marca_branca, 'MAG'), encoding='utf-8')
    marca_branca.resize((int(marca_branca.width * 60 / marca_branca.height), 60), Image.LANCZOS).save(IMAGES / 'logo.png', optimize=True)
    (IMAGES / 'logo_blue.svg').write_text(svg_com_png(original, 'Grupo MAG Móveis Corporativos'), encoding='utf-8')
    original.save(IMAGES / 'logo_blue.png', optimize=True)   # logo embutido nos e-mails
    icone(512, marca_branca).save(IMAGES / 'favicon.png', optimize=True)
    icone(512, marca_branca, arredondado=False).save(IMAGES / 'apple-touch-icon.png', optimize=True)
    icone(192, marca_branca).save(IMAGES / 'icon-192.png', optimize=True)
    icone(512, marca_branca).save(IMAGES / 'icon-512.png', optimize=True)
    icone(48, marca_branca).save(PUBLIC / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])

    thumb = miniatura_tema()
    thumb.save(IMAGES / 'background-default.png', optimize=True)
    thumb.save(IMAGES / 'background-minimal.png', optimize=True)

    for p in sorted(list(MAG_DIR.iterdir()) + [IMAGES / n for n in (
            'logo.svg', 'logo.png', 'logo_blue.svg', 'logo_blue.png', 'favicon.png', 'apple-touch-icon.png',
            'icon-192.png', 'icon-512.png', 'background-default.png', 'background-minimal.png')] + [PUBLIC / 'favicon.ico']):
        print(f'{p.relative_to(BASE)}  {p.stat().st_size} bytes')


if __name__ == '__main__':
    main()
