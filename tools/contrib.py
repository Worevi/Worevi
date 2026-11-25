# Gráfico de contribuições em estilo aquático: lê o calendário pela API GraphQL do GitHub e desenha assets/contribuicoes.svg.
# Corre localmente (token do gh) ou na GitHub Action (GITHUB_TOKEN). Sem dependências além do Python.
import os, json, urllib.request, subprocess, datetime, random, sys
LOGIN = "Worevi"
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), "assets", "contribuicoes.svg")
W = 1200; GOLD, TEAL, TEAL2, TEALB, INK, DEEP = "#f2b92a", "#19a3ad", "#0e7c86", "#2fd3de", "#040a14", "#07192b"
FONT = "'Segoe UI',Helvetica,Arial,sans-serif"
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
rnd = random.Random(11)

def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t: return t
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, shell=True).stdout.strip()

def calendar():
    q = '{ user(login: "%s") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }' % LOGIN
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": q}).encode(),
                                 headers={"Authorization": "bearer " + token(), "Content-Type": "application/json", "User-Agent": "worevi-profile"})
    with urllib.request.urlopen(req, timeout=30) as r: d = json.load(r)
    cal = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[(x["date"], x["contributionCount"]) for x in w["contributionDays"]] for w in cal["weeks"]]
    return cal["totalContributions"], weeks

total, weeks = calendar()
counts = [c for w in weeks for _, c in w]; mx = max(counts) or 1
def level(c):
    if c <= 0: return 0
    return 1 + min(3, int(3 * c / mx + 0.999) - 1) if mx > 1 else 1
cols = len(weeks); cell, gap = 16, 4; step = cell + gap
gx = (W - cols * step + gap) / 2; gy = 84; gh = 7 * step - gap
H = 350
body = []
# feixes de luz
for i in range(5):
    x = 100 + i * 250; w = rnd.uniform(60, 120); d = rnd.uniform(9, 15)
    body.append(f'<polygon points="{x-w/2:.0f},0 {x+w/2:.0f},0 {x+w*1.6:.0f},{H} {x-w*1.6:.0f},{H}" fill="url(#ray)" opacity=".4">'
                f'<animateTransform attributeName="transform" type="rotate" values="-3 {x} 0;3 {x} 0;-3 {x} 0" dur="{d:.1f}s" repeatCount="indefinite"/></polygon>')
body.append(f'<text class="k" x="56" y="46">CONTRIBUIÇÕES · ÚLTIMOS 12 MESES</text>')
body.append(f'<text class="k" x="{W-56}" y="46" text-anchor="end" style="opacity:.9"><tspan fill="{GOLD}">{total}</tspan> NO TOTAL</text>')
fills = {0: ("#ffffff", .05), 1: (TEAL2, .5), 2: (TEAL, .75), 3: (TEALB, .9), 4: (GOLD, 1)}
bub = []; last_month = None
for ci, w in enumerate(weeks):
    x = gx + ci * step
    # etiqueta do mês na primeira semana de cada mês
    m = int(w[0][0][5:7])
    if m != last_month and ci < cols - 2:
        body.append(f'<text x="{x:.0f}" y="{gy+gh+24}" style="font:600 11px {FONT};letter-spacing:.18em;fill:#9fb3c8">{MESES[m-1].upper()}</text>'); last_month = m
    for ri, (date, c) in enumerate(w):
        y = gy + ri * step; lv = level(c); col, op = fills[lv]
        if lv == 0:
            body.append(f'<rect x="{x:.0f}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{col}" fill-opacity="{op}"/>')
        else:
            dl = rnd.uniform(0, 4)
            body.append(f'<rect x="{x-3:.0f}" y="{y-3}" width="{cell+6}" height="{cell+6}" rx="7" fill="{col}" opacity=".25" filter="url(#soft)"/>'
                        f'<rect class="c" x="{x:.0f}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{col}" fill-opacity="{op}" style="animation-delay:-{dl:.1f}s"><title>{date}: {c}</title></rect>')
            if lv >= 3:
                d = rnd.uniform(6, 10); b = -rnd.uniform(0, d)
                bub.append(f'<circle cx="{x+cell/2:.0f}" cy="{y}" r="{rnd.uniform(1.5,3):.1f}" fill="none" stroke="{col}" stroke-opacity=".7" stroke-width="1.2">'
                           f'<animate attributeName="cy" from="{y}" to="{gy-40}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                           f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.8;1" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
body += bub
# legenda
lx = W - 56 - 5 * 22; ly = gy + gh + 46   # linha própria, abaixo dos meses
body.append(f'<text x="{lx-10}" y="{ly+12}" text-anchor="end" style="font:600 11px {FONT};letter-spacing:.18em;fill:#9fb3c8">MENOS</text>')
for i in range(5):
    col, op = fills[i]; body.append(f'<rect x="{lx+i*22}" y="{ly}" width="{cell}" height="{cell}" rx="4" fill="{col}" fill-opacity="{op}"/>')
body.append(f'<text x="{lx+5*22+4}" y="{ly+12}" style="font:600 11px {FONT};letter-spacing:.18em;fill:#9fb3c8">MAIS</text>')
# ondas no fundo
def wave(y, amp, lam, x0):
    p = f"M{x0},{y}"; x = x0
    while x < x0 + 2 * W: p += f" q{lam/4},{-amp} {lam/2},0 q{lam/4},{amp} {lam/2},0"; x += lam
    return p + f" V{H+10} H{x0} Z"
body.append(f'<path fill="{TEAL2}" opacity=".3" d="{wave(H-26, 5, 200, -W)}"><animateTransform attributeName="transform" type="translate" from="0 0" to="{W} 0" dur="11s" repeatCount="indefinite"/></path>')
body.append(f'<path fill="{TEAL}" opacity=".22" d="{wave(H-18, 4, 150, 0)}"><animateTransform attributeName="transform" type="translate" from="0 0" to="-{W} 0" dur="8s" repeatCount="indefinite"/></path>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Contribuições no GitHub nos últimos 12 meses: {total}">'
       f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{INK}"/></linearGradient>'
       f'<linearGradient id="ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity=".35"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>'
       f'<filter id="soft"><feGaussianBlur stdDeviation="3"/></filter><clipPath id="clip"><rect width="{W}" height="{H}" rx="26"/></clipPath></defs>'
       f'<style>.k{{font:600 12px {FONT};letter-spacing:.32em;fill:#fff;opacity:.6}}.c{{animation:p 4s ease-in-out infinite}}@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}</style>'
       f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{"".join(body)}</g></svg>')
open(OUT, "w", encoding="utf-8").write(svg)
print("contribuicoes.svg", len(svg) // 1024, "KB", "total", total, "semanas", cols, "máx/dia", mx)
