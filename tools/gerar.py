# Perfil GitHub da Worevi: cada secção é um SVG animado (SMIL + CSS, funciona dentro de <img> no GitHub).
# Tema: debaixo de água — cáusticas, bolhas, ondas, aquários de vidro, peixes em silhueta. Paleta: azul profundo, teal, ouro da marca.
import re, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), "assets"); os.makedirs(OUT, exist_ok=True)
WM = r"C:\Users\Gui\Desktop\aa\worevi-carrossel\wordmark-branco.svg"
PB = r"C:\Users\Gui\Desktop\aa\Site\marketing\logo\piscobrilho-logo-horizontal-branco.svg"
W = 1200
GOLD, TEAL, TEAL2, INK, DEEP = "#f2b92a", "#19a3ad", "#0e7c86", "#040a14", "#07192b"
FONT = "'Segoe UI',Helvetica,Arial,sans-serif"   # aspas simples: também é usado dentro de style="..."
rnd = random.Random(7)

def wordmark():
    s = open(WM, encoding="latin-1").read()
    ds = [re.sub(r"\s+", " ", d).strip() for d in re.findall(r'<path[^>]*?\bd="([^"]+)"', s)][:7]
    # 0–5 são as letras (y 119–403); 6 é a bola do i (y 0–92), em ouro como na marca; os restantes 53 são a linha pequena de serviços
    return "".join(f'<path d="{d}"/>' for d in ds[:6]) + f'<path style="fill:{GOLD}" d="{ds[6]}"/>'
def piscobrilho():
    s = open(PB, encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    return vb, "".join(re.findall(r"<path[^>]*/>", s))

def wave(y, amp, lam, width=2 * W, x0=0):
    # onda contínua em curvas quadráticas; width = 2× largura para o loop ser perfeito
    p = f"M{x0},{y}"; x = x0
    while x < x0 + width:
        p += f" q{lam/4},{-amp} {lam/2},0 q{lam/4},{amp} {lam/2},0"; x += lam
    return p + f" V2000 H{x0} Z"
def wave_in(x, y, amp, lam, color, op, dur, right=True, stroke=False):
    # onda que cobre sempre [x, x+W] durante todo o loop: para a direita começa em x-W e anda +W; para a esquerda começa em x e anda -W.
    # lam tem de dividir W para a emenda do loop ser invisível.
    x0 = x - W if right else x; a, b = (0, W) if right else (0, -W)
    d = wave(y, amp, lam, x0=x0)
    paint = f'fill="none" stroke="{color}" stroke-width="1.5"' if stroke else f'fill="{color}"'
    if stroke: d = d.split(" V")[0]
    return (f'<path {paint} opacity="{op}" d="{d}"><animateTransform attributeName="transform" type="translate" from="{a} 0" to="{b} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
def bubbles(n, x0, x1, y0, y1, rmin=2, rmax=7, dur=(9, 18), op=.55, color="#fff"):
    out = ""
    for _ in range(n):
        x = rnd.uniform(x0, x1); r = rnd.uniform(rmin, rmax); d = rnd.uniform(*dur); b = -rnd.uniform(0, d)
        sw = rnd.uniform(6, 18)
        out += (f'<circle cx="{x:.0f}" cy="{y0}" r="{r:.1f}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.2">'
                f'<animate attributeName="cy" from="{y0}" to="{y1}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="cx" values="{x:.0f};{x+sw:.0f};{x:.0f}" dur="{d/2.3:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
    return out
def caustics(H, n=6):
    # feixes de luz a entrar pela superfície, a balançar devagar
    out = ""
    for i in range(n):
        x = 80 + i * (W - 160) / (n - 1); w = rnd.uniform(60, 140); d = rnd.uniform(9, 15); b = -rnd.uniform(0, 10)
        out += (f'<polygon points="{x-w/2:.0f},0 {x+w/2:.0f},0 {x+w*1.6:.0f},{H} {x-w*1.6:.0f},{H}" fill="url(#ray)" opacity=".5">'
                f'<animateTransform attributeName="transform" type="rotate" values="-3 {x:.0f} 0;3 {x:.0f} 0;-3 {x:.0f} 0" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values=".25;.6;.25" dur="{d*0.7:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></polygon>')
    return out
def fish(x, y, size, dur, flip=False, op=.16, color=TEAL):
    # silhueta simples: corpo + cauda a abanar; atravessa o ecrã
    s = size; sx = -1 if flip else 1
    frm, to = (W + 200, -300) if flip else (-300, W + 200)
    return (f'<g opacity="{op}"><g transform="translate({frm},{y})"><animateTransform attributeName="transform" type="translate" from="{frm} {y}" to="{to} {y}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<g transform="scale({sx},1)"><g><animateTransform attributeName="transform" type="translate" values="0 0;0 -{s*0.18:.0f};0 0" dur="3.2s" repeatCount="indefinite"/>'
            f'<ellipse cx="0" cy="0" rx="{s}" ry="{s*0.36:.0f}" fill="{color}"/>'
            f'<path d="M{-s*0.9:.0f},0 L{-s*1.5:.0f},{-s*0.42:.0f} L{-s*1.35:.0f},0 L{-s*1.5:.0f},{s*0.42:.0f} Z" fill="{color}">'
            f'<animateTransform attributeName="transform" type="rotate" values="-14 {-s*0.9:.0f} 0;14 {-s*0.9:.0f} 0;-14 {-s*0.9:.0f} 0" dur=".9s" repeatCount="indefinite"/></path>'
            f'<circle cx="{s*0.62:.0f}" cy="{-s*0.08:.0f}" r="{max(1.5,s*0.05):.1f}" fill="{INK}"/></g></g></g></g>')
def defs(H, extra=""):
    return (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{INK}"/></linearGradient>'
            f'<linearGradient id="ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity=".35"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="mfade"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
            f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="26"/></clipPath>'
            f'<filter id="water" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".012 .05" numOctaves="2" seed="3" result="n">'
            f'<animate attributeName="baseFrequency" values=".012 .05;.016 .06;.012 .05" dur="7s" repeatCount="indefinite"/></feTurbulence>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="18" xChannelSelector="R" yChannelSelector="G"/></filter>'
            f'<filter id="blur"><feGaussianBlur stdDeviation="1.2"/></filter>{extra}</defs>')
def svg(H, body, label, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
            f'{defs(H)}<style>.k{{font:600 12px {FONT};letter-spacing:.32em;fill:#fff;opacity:.6}}.h{{font:700 30px {FONT};letter-spacing:-.02em;fill:#fff}}'
            f'.t{{font:600 19px {FONT};fill:#fff}}.s{{font:400 14px {FONT};fill:#9fb3c8}}.g{{fill:{GOLD}}}{style}</style>'
            f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{body}</g></svg>')
def save(name, content):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(content); print(name, len(content) // 1024, "KB")

# ---------- 1. cabeçalho: superfície com ondas, cáusticas, wordmark com reflexo na água, peixes, bolhas ----------
H = 520; letters = wordmark(); sc = 600 / 1600; wx = (W - 600) / 2; wy = 150
services = ["Fotografia e vídeo", "Redes sociais", "Podcast e cortes", "Sites e plataformas"]; T = 3.4; n = len(services)
words = "".join(f'<text class="w" x="{W/2}" y="440" text-anchor="middle" style="animation-delay:{i*T}s">{t}</text>' for i, t in enumerate(services))
style = (f'.wm path{{fill:#fff;opacity:0;transform:translateY(16px);animation:up 1s cubic-bezier(.2,.7,.2,1) forwards}}@keyframes up{{to{{opacity:1;transform:none}}}}'
         f'.w{{font:500 21px {FONT};fill:#fff;opacity:0;animation:w {n*T}s infinite}}@keyframes w{{0%{{opacity:0;transform:translateY(8px)}}6%{{opacity:1;transform:none}}{100/n-4:.1f}%{{opacity:1}}{100/n:.1f}%{{opacity:0;transform:translateY(-8px)}}100%{{opacity:0}}}}'
         f'.ln{{stroke:{GOLD};stroke-width:2;stroke-linecap:round;stroke-dasharray:600;stroke-dashoffset:600;animation:ln 1.8s .6s cubic-bezier(.2,.7,.2,1) forwards}}@keyframes ln{{to{{stroke-dashoffset:0}}}}'
         f'.dot{{animation:bl 2.4s ease-in-out infinite}}@keyframes bl{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}')
body = caustics(H)
body += fish(0, 300, 26, 38) + fish(0, 190, 16, 52, flip=True) + fish(0, 440, 20, 46) + fish(0, 120, 12, 61, flip=True, op=.1)
body += bubbles(26, 40, W - 40, H + 10, -20, 2, 7, (10, 20), .35)
# superfície da água no topo: duas ondas a deslizar em sentidos diferentes
body += wave_in(0, 30, 5, 200, TEAL, .35, 9, right=True, stroke=True) + wave_in(0, 40, 3, 150, "#fff", .2, 13, right=False, stroke=True)
# wordmark com reflexo distorcido pela água
body += f'<g class="wm" transform="translate({wx:.1f},{wy}) scale({sc:.5f})">{letters}</g>'
# reflexo: o fundo das letras (y=403 na caixa) fica logo abaixo da linha dourada (y≈314), invertido e esmagado a 75 %
rimg = (f'<g mask="url(#mfade)" opacity=".45" filter="url(#water)"><g transform="translate({wx:.1f},{314 + 403*sc*0.75:.1f}) scale({sc:.5f},{-sc*0.75:.5f})">'
        + letters.replace("<path ", f'<path fill="#fff" ') + "</g></g>")
body += rimg
body += f'<line class="ln" x1="{wx:.0f}" y1="308" x2="{wx+600:.0f}" y2="308"/>'
body += words
body += (f'<text class="k" x="56" y="62">ESTÚDIO CRIATIVO · PORTUGAL</text>'
         f'<g transform="translate({W-56},62)"><circle class="dot g" cx="-100" cy="-4" r="4"/><text class="k" x="-86" y="0">DISPONÍVEL</text></g>'
         f'<text class="k" x="56" y="{H-40}">IMAGEM DE CINEMA · RITMO DE REDES SOCIAIS</text><text class="k" x="{W-56}" y="{H-40}" text-anchor="end">worevi.com</text>')
save("header.svg", svg(H, body, "Worevi — estúdio criativo", style))

# ---------- 2. serviços: quatro aquários de vidro, cada um com a sua água, bolhas e um ícone animado ----------
H = 330; cw = 258; gap = (W - 4 * cw - 2 * 56) / 3; icons = []
def icon_camera(): return (f'<rect x="-28" y="-16" width="56" height="38" rx="8" fill="none" stroke="#fff" stroke-width="2.2"/><rect x="-10" y="-24" width="20" height="9" rx="3" fill="none" stroke="#fff" stroke-width="2.2"/>'
                           f'<circle cx="0" cy="3" r="11" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-dasharray="6 5"><animateTransform attributeName="transform" type="rotate" from="0 0 3" to="360 0 3" dur="9s" repeatCount="indefinite"/></circle><circle cx="0" cy="3" r="4" fill="{GOLD}"/>')
def icon_social(): return (''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="none" stroke="#fff" stroke-width="2.2"/>' for x, y in [(-22, 10), (0, -16), (22, 10)]) +
                           f'<path d="M-17,6 L-5,-11 M5,-11 L17,6 M-16,10 L16,10" stroke="{GOLD}" stroke-width="2" stroke-dasharray="90" stroke-dashoffset="90"><animate attributeName="stroke-dashoffset" values="90;0;0;90" keyTimes="0;.4;.7;1" dur="4s" repeatCount="indefinite"/></path>')
def icon_mic(): return (f'<rect x="-9" y="-26" width="18" height="34" rx="9" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M-18,0 a18,18 0 0 0 36,0 M0,18 V28 M-10,28 H10" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
                        + ''.join(f'<path d="M{x},-14 a{r},{r} 0 0 1 0,28" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;.9;0" dur="2.2s" begin="{i*0.5}s" repeatCount="indefinite"/></path>' for i, (x, r) in enumerate([(22, 10), (32, 15)])))
def icon_web(): return (f'<rect x="-30" y="-20" width="60" height="42" rx="7" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M-30,-9 H30" stroke="#fff" stroke-width="2.2"/><circle cx="-22" cy="-14.5" r="2" fill="{GOLD}"/><circle cx="-15" cy="-14.5" r="2" fill="{GOLD}"/>'
                        f'<path d="M-20,2 H20 M-20,10 H6" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="40" stroke-dashoffset="40"><animate attributeName="stroke-dashoffset" values="40;0;0;40" keyTimes="0;.35;.75;1" dur="3.6s" repeatCount="indefinite"/></path>')
cards = [("Fotografia e vídeo", "Produto, retrato, editorial\ne vídeo para marcas", icon_camera()),
         ("Redes sociais", "Conteúdo todos os meses,\ncom calendário cumprido", icon_social()),
         ("Podcast e cortes", "Gravação, edição\ne cortes verticais", icon_mic()),
         ("Sites e plataformas", "Sites rápidos, lojas\ne painéis de gestão", icon_web())]
body = caustics(H, 4)
for i, (t, s, ic) in enumerate(cards):
    x = 56 + i * (cw + gap); y = 34; ch = H - 68
    body += f'<g clip-path="url(#c{i})"><clipPath id="c{i}"><rect x="{x:.0f}" y="{y}" width="{cw}" height="{ch}" rx="22"/></clipPath>'
    body += f'<rect x="{x:.0f}" y="{y}" width="{cw}" height="{ch}" rx="22" fill="#fff" fill-opacity=".035"/>'
    # água dentro do aquário: enche até 58 % com onda a mexer, duas camadas
    wl = y + ch * 0.42
    body += wave_in(x, wl, 6, 200, TEAL2, .28, 7 + i, right=True) + wave_in(x, wl, 4, 120, TEAL, .22, 5 + i, right=False)
    body += bubbles(7, x + 20, x + cw - 20, y + ch, wl + 6, 1.5, 4, (5, 9), .5)
    body += f'<rect x="{x:.0f}" y="{y}" width="{cw}" height="{ch}" rx="22" fill="url(#glass)"/></g>'
    body += f'<rect x="{x:.0f}" y="{y}" width="{cw}" height="{ch}" rx="22" fill="none" stroke="#fff" stroke-opacity=".14"/>'
    body += f'<g transform="translate({x+cw/2:.0f},{y+72})">{ic}</g>'
    body += f'<text class="t" x="{x+cw/2:.0f}" y="{y+ch-78}" text-anchor="middle">{t}</text>'
    for j, ln in enumerate(s.split("\n")):
        body += f'<text class="s" x="{x+cw/2:.0f}" y="{y+ch-52+j*20}" text-anchor="middle">{ln}</text>'
save("servicos.svg", svg(H, body, "Serviços Worevi"))

# ---------- 3. método: corrente de água a ligar quatro passos com ondulações ----------
H = 270; steps = [("01", "Percebemos o negócio", "antes de pegar na câmara"), ("02", "Decidimos tudo", "antes do dia da gravação"),
                  ("03", "Chegamos com tudo", "o que é preciso"), ("04", "Edição, cor", "e o botão de publicar")]
body = caustics(H, 3); xs = [56 + 120 + i * ((W - 112 - 240) / 3) for i in range(4)]; cy = 118
body += f'<text class="k" x="56" y="44">COMO TRABALHAMOS · DO BRIEFING AO AR, EM DIAS</text>'
# corrente: linha ondulada com traços a correr
cur = "M" + " ".join(f"{xs[0]-60},{cy}" if k == 0 else f"q{(xs[1]-xs[0])/4:.0f},-14 {(xs[1]-xs[0])/2:.0f},0 q{(xs[1]-xs[0])/4:.0f},14 {(xs[1]-xs[0])/2:.0f},0" for k in range(4))
body += (f'<path d="{cur}" fill="none" stroke="{TEAL}" stroke-opacity=".35" stroke-width="2"/>'
         f'<path d="{cur}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-linecap="round" stroke-dasharray="10 18"><animate attributeName="stroke-dashoffset" from="0" to="-280" dur="6s" repeatCount="indefinite"/></path>')
for i, (num, a, b) in enumerate(steps):
    x = xs[i]
    for k in range(3):
        body += (f'<circle cx="{x:.0f}" cy="{cy}" r="22" fill="none" stroke="{GOLD}" stroke-width="1.5" opacity="0">'
                 f'<animate attributeName="r" from="22" to="58" dur="3s" begin="{i*0.6+k:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="3s" begin="{i*0.6+k:.1f}s" repeatCount="indefinite"/></circle>')
    body += (f'<circle cx="{x:.0f}" cy="{cy}" r="24" fill="{INK}" stroke="{GOLD}" stroke-width="2"/>'
             f'<text x="{x:.0f}" y="{cy+5}" text-anchor="middle" style="font:700 14px {FONT};fill:{GOLD}">{num}</text>'
             f'<text class="t" x="{x:.0f}" y="{cy+70}" text-anchor="middle">{a}</text><text class="s" x="{x:.0f}" y="{cy+94}" text-anchor="middle">{b}</text>')
body += bubbles(10, 40, W - 40, H + 10, -10, 1.5, 4, (8, 14), .3)
save("metodo.svg", svg(H, body, "Como trabalhamos"))

# ---------- 4. projetos: dois cartões, um com o logótipo Piscobrilho (gotas de água), outro com o wordmark Worevi ----------
H = 300; vb, pbp = piscobrilho(); vx, vy, vw, vh = map(float, vb.split())
body = caustics(H, 3) + f'<text class="k" x="56" y="44">PROJETOS</text>'
cw2 = (W - 112 - 28) / 2
for i, (title, sub, url) in enumerate([("Piscobrilho", "Loja online de cuidado automóvel · marca, fotografia de produto e plataforma", "piscobrilho.com · em breve"),
                                       ("Worevi", "O nosso site, com o portefólio e a forma como trabalhamos", "worevi.com")]):
    x = 56 + i * (cw2 + 28); y = 64; ch = H - 64 - 34
    body += f'<clipPath id="p{i}"><rect x="{x:.0f}" y="{y}" width="{cw2:.0f}" height="{ch}" rx="22"/></clipPath><g clip-path="url(#p{i})">'
    body += f'<rect x="{x:.0f}" y="{y}" width="{cw2:.0f}" height="{ch}" rx="22" fill="{"#101010" if i == 0 else "#0b2238"}"/>'
    # água a encher o fundo do cartão
    wl = y + ch * 0.68
    body += wave_in(x, wl, 5, 150, TEAL2, .35, 8, right=True) + wave_in(x, wl, 3, 100, TEAL, .25, 6, right=False)
    body += bubbles(8, x + 30, x + cw2 - 30, y + ch, wl + 4, 1.5, 4, (6, 10), .45)
    if i == 0:
        s = 150 / vw
        body += f'<g fill="#fff" transform="translate({x+32:.0f},{y+34}) scale({s:.4f}) translate({-vx:.2f},{-vy:.2f})">{pbp}</g>'
        # gotas de água a cair no logótipo, de vez em quando
        for k in range(3):
            gx = x + 60 + k * 50
            body += (f'<circle cx="{gx:.0f}" cy="{y+10}" r="2.5" fill="{TEAL}" opacity="0"><animate attributeName="cy" from="{y+10}" to="{wl}" dur="1.4s" begin="{k*1.7+0.4:.1f}s;{k*1.7+0.4:.1f}s+5.2s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.1;.9;1" dur="1.4s" begin="{k*1.7+0.4:.1f}s" repeatCount="indefinite"/></circle>')
    else:
        body += f'<g transform="translate({x+32:.0f},{y+26}) scale({150/1600:.4f})" fill="#fff">{letters}</g>'
    body += f'<rect x="{x:.0f}" y="{y}" width="{cw2:.0f}" height="{ch}" rx="22" fill="url(#glass)"/></g>'
    body += f'<rect x="{x:.0f}" y="{y}" width="{cw2:.0f}" height="{ch}" rx="22" fill="none" stroke="#fff" stroke-opacity=".14"/>'
    body += f'<text class="t" x="{x+32:.0f}" y="{y+ch-58}">{title}</text><text class="s" x="{x+32:.0f}" y="{y+ch-36}">{sub}</text>'
    body += f'<text x="{x+32:.0f}" y="{y+ch-14}" style="font:600 12px {FONT};letter-spacing:.22em;fill:{GOLD}">{url.upper()}</text>'
save("projetos.svg", svg(H, body, "Projetos"))

# ---------- 5. contacto: superfície de água calma com gotas a cair e anéis a abrir ----------
H = 200; body = caustics(H, 3)
for k in range(5):
    gx = 120 + k * 240; b = k * 1.3
    body += (f'<circle cx="{gx}" cy="-6" r="2.5" fill="{TEAL}"><animate attributeName="cy" from="-6" to="112" dur="1.1s" begin="{b:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="1.1s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
    for r0 in (0, 1):
        body += (f'<ellipse cx="{gx}" cy="112" rx="4" ry="1.5" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity="0">'
                 f'<animate attributeName="rx" from="4" to="90" dur="2.4s" begin="{b+1.1+r0*0.35:.2f}s" repeatCount="indefinite"/><animate attributeName="ry" from="1.5" to="30" dur="2.4s" begin="{b+1.1+r0*0.35:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".8;0" dur="2.4s" begin="{b+1.1+r0*0.35:.2f}s" repeatCount="indefinite"/></ellipse>')
body += f'<line x1="56" y1="112" x2="{W-56}" y2="112" stroke="{TEAL}" stroke-opacity=".25"/>'
body += f'<text class="k" x="56" y="44">CONTACTO</text>'
body += (f'<text class="h" x="{W/2}" y="152" text-anchor="middle" style="font-size:24px">geral@worevi.com'
         f'<tspan fill="{GOLD}"> · </tspan>+351 910 861 499<tspan fill="{GOLD}"> · </tspan>worevi.com</text>')
save("contacto.svg", svg(H, body, "Contacto"))

# ---------- 6. rodapé: três camadas de ondas, peixes e os serviços a passar ----------
H = 150; body = ""
body += fish(0, 56, 14, 44, op=.14) + fish(0, 40, 9, 58, flip=True, op=.1)
items = (" · ".join(["Fotografia", "Vídeo", "Redes sociais", "Podcast", "Cortes", "Sites", "Plataformas", "Motion", "Cor", "Edição"]) + " · ").upper()
body += (f'<g><text x="0" y="52" style="font:600 12px {FONT};letter-spacing:.3em;fill:#fff;opacity:.55" textLength="{2*W}" lengthAdjust="spacing">{items*3}</text>'
         f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{W} 0" dur="30s" repeatCount="indefinite"/></g>')
body += wave_in(0, 96, 9, 300, TEAL2, .45, 12, right=True) + wave_in(0, 106, 7, 240, TEAL, .4, 9, right=False) + wave_in(0, 118, 5, 150, GOLD, .75, 7, right=True, stroke=True)
body += bubbles(12, 40, W - 40, H + 10, 60, 1.5, 4, (7, 12), .4)
save("footer.svg", svg(H, body, "Worevi"))
