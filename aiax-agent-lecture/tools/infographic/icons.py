# Simple flat icons drawn in a 120x120 box. c = main color.
INK = "#2b2d42"

def lamp(c):
    return f'''<path d="M18 78 Q60 100 96 78 L88 70 Q60 82 30 70 Z" fill="{c}"/>
<ellipse cx="58" cy="70" rx="34" ry="14" fill="{c}"/>
<path d="M90 68 Q112 58 114 48 Q104 56 92 60" fill="{c}"/>
<path d="M24 68 Q8 66 10 54 Q14 62 28 62" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round"/>
<rect x="48" y="86" width="22" height="8" rx="3" fill="{c}"/><rect x="40" y="94" width="38" height="8" rx="4" fill="{c}"/>
<path d="M58 56 Q50 40 62 32 Q74 24 66 10" fill="none" stroke="#9aa5b1" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 9"/>'''

def genie(c):
    return f'''<path d="M60 70 Q30 80 40 100 Q50 116 72 108 Q56 104 58 94 Q60 84 76 78 Z" fill="{c}" opacity=".55"/>
<circle cx="60" cy="42" r="26" fill="{c}"/>
<circle cx="51" cy="40" r="4" fill="#fff"/><circle cx="69" cy="40" r="4" fill="#fff"/>
<path d="M48 52 Q60 62 72 52" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
<path d="M38 24 Q60 4 82 24 Q60 16 38 24 Z" fill="{INK}"/>'''

def question(c):
    return f'''<circle cx="60" cy="60" r="46" fill="{c}"/>
<path d="M44 46 Q44 28 60 28 Q78 28 78 44 Q78 56 64 60 L64 72" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/>
<circle cx="64" cy="88" r="6" fill="#fff"/>'''

def tag(c):
    return f'''<path d="M20 30 L70 30 L102 60 L70 90 L20 90 Z" fill="{c}"/><circle cx="38" cy="60" r="8" fill="#fff"/>
<text x="64" y="68" font-size="22" font-weight="800" fill="#fff" text-anchor="middle">AI</text>'''

def snow(c):
    s = ""
    for a in (0, 60, 120):
        s += f'<line x1="60" y1="14" x2="60" y2="106" stroke="{c}" stroke-width="8" stroke-linecap="round" transform="rotate({a} 60 60)"/>'
        s += f'<path d="M48 24 L60 36 L72 24" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round" transform="rotate({a} 60 60)"/>'
        s += f'<path d="M48 96 L60 84 L72 96" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round" transform="rotate({a} 60 60)"/>'
    return s

def photos(c):
    return f'''<rect x="14" y="30" width="62" height="50" rx="8" fill="{c}" opacity=".45"/>
<rect x="30" y="42" width="66" height="54" rx="8" fill="{c}"/>
<circle cx="50" cy="60" r="7" fill="#fff"/><path d="M36 90 L56 70 L68 80 L80 66 L92 90 Z" fill="#fff"/>
<circle cx="96" cy="30" r="16" fill="#ffd166"/><path d="M90 30 L95 35 L104 25" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'''

def board(c):
    s = f'<rect x="16" y="16" width="88" height="88" rx="8" fill="#f2d49b"/>'
    for i in range(1,4):
        s += f'<line x1="{16+22*i}" y1="16" x2="{16+22*i}" y2="104" stroke="#8a6d3b" stroke-width="2"/>'
        s += f'<line x1="16" y1="{16+22*i}" x2="104" y2="{16+22*i}" stroke="#8a6d3b" stroke-width="2"/>'
    for x,y,f in ((38,38,INK),(60,60,"#fff"),(82,38,INK),(60,82,"#fff"),(38,82,INK)):
        s += f'<circle cx="{x}" cy="{y}" r="9" fill="{f}" stroke="{INK}" stroke-width="2"/>'
    return s

def bubble(c):
    return f'''<path d="M14 26 Q14 14 26 14 L94 14 Q106 14 106 26 L106 70 Q106 82 94 82 L50 82 L28 104 L32 82 L26 82 Q14 82 14 70 Z" fill="{c}"/>
<circle cx="40" cy="48" r="7" fill="#fff"/><circle cx="60" cy="48" r="7" fill="#fff"/><circle cx="80" cy="48" r="7" fill="#fff"/>'''

def robot(c):
    return f'''<line x1="60" y1="10" x2="60" y2="24" stroke="{c}" stroke-width="5"/><circle cx="60" cy="10" r="6" fill="#ef476f"/>
<rect x="28" y="24" width="64" height="44" rx="12" fill="{c}"/>
<circle cx="46" cy="44" r="7" fill="#fff"/><circle cx="74" cy="44" r="7" fill="#fff"/>
<rect x="48" y="56" width="24" height="5" rx="2" fill="#fff"/>
<rect x="36" y="72" width="48" height="34" rx="8" fill="{c}" opacity=".8"/>
<rect x="14" y="76" width="16" height="8" rx="4" fill="{c}"/><rect x="90" y="76" width="16" height="8" rx="4" fill="{c}"/>'''

def magnifier(c):
    return f'''<circle cx="50" cy="50" r="30" fill="#fff" stroke="{c}" stroke-width="10"/>
<line x1="72" y1="72" x2="104" y2="104" stroke="{c}" stroke-width="14" stroke-linecap="round"/>
<path d="M36 42 Q42 32 52 32" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round" opacity=".5"/>'''

def wish(c):
    return f'''<path d="M60 12 L72 44 L106 46 L80 66 L90 100 L60 80 L30 100 L40 66 L14 46 L48 44 Z" fill="{c}"/>'''

def brain(c):
    return f'''<path d="M60 22 Q40 10 28 26 Q12 30 16 50 Q8 66 22 78 Q24 98 44 98 Q54 108 60 98 Z" fill="{c}"/>
<path d="M60 22 Q80 10 92 26 Q108 30 104 50 Q112 66 98 78 Q96 98 76 98 Q66 108 60 98 Z" fill="{c}" opacity=".8"/>
<path d="M60 24 L60 98 M34 48 Q44 52 40 64 M86 48 Q76 52 80 64" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'''

def blocks(c):
    return f'''<rect x="14" y="64" width="44" height="34" rx="4" fill="#ef476f"/><rect x="62" y="64" width="44" height="34" rx="4" fill="{c}"/>
<rect x="38" y="28" width="44" height="34" rx="4" fill="#ffd166"/>
<circle cx="28" cy="62" r="5" fill="#ef476f"/><circle cx="44" cy="62" r="5" fill="#ef476f"/>
<circle cx="76" cy="62" r="5" fill="{c}"/><circle cx="92" cy="62" r="5" fill="{c}"/>
<circle cx="52" cy="26" r="5" fill="#ffd166"/><circle cx="68" cy="26" r="5" fill="#ffd166"/>'''

def armleg(c):
    return f'''<circle cx="60" cy="24" r="14" fill="{c}"/>
<rect x="44" y="40" width="32" height="38" rx="8" fill="{c}"/>
<path d="M44 48 L18 62 L14 50" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"/>
<path d="M76 48 L100 36" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"/>
<rect x="96" y="22" width="16" height="20" rx="3" fill="#ffd166"/>
<path d="M52 78 L46 108 M68 78 L74 108" stroke="{c}" stroke-width="10" stroke-linecap="round"/>'''

def ladder(c):
    return f'''<rect x="14" y="80" width="26" height="26" rx="4" fill="#9aa5b1"/>
<rect x="46" y="58" width="26" height="48" rx="4" fill="{c}" opacity=".7"/>
<rect x="78" y="22" width="26" height="84" rx="4" fill="{c}"/>
<path d="M22 70 L90 14" stroke="#ef476f" stroke-width="5" stroke-dasharray="6 6"/>'''

def spiral(c):
    return f'''<circle cx="60" cy="60" r="48" fill="{INK}"/>
<path d="M60 60 m0 -6 a6 6 0 1 1 -6 6 a12 12 0 1 1 12 12 a20 20 0 1 1 -20 -20 a30 30 0 1 1 30 30" fill="none" stroke="#ffd166" stroke-width="5" stroke-linecap="round"/>'''

def spark(c):
    return f'''<path d="M60 10 L68 50 L108 60 L68 70 L60 110 L52 70 L12 60 L52 50 Z" fill="{c}"/>
<circle cx="96" cy="22" r="6" fill="{c}" opacity=".6"/><circle cx="22" cy="98" r="5" fill="{c}" opacity=".6"/>'''

def baby(c):
    return f'''<circle cx="60" cy="56" r="34" fill="#ffe0bd"/>
<circle cx="48" cy="54" r="4" fill="{INK}"/><circle cx="72" cy="54" r="4" fill="{INK}"/>
<circle cx="60" cy="70" r="5" fill="{c}"/><path d="M60 22 Q66 14 70 20" fill="none" stroke="{INK}" stroke-width="3"/>
<path d="M90 30 Q112 30 112 46 Q112 60 96 60" fill="#fff" stroke="{c}" stroke-width="3"/><text x="102" y="50" font-size="13" text-anchor="middle" fill="{c}" font-weight="700">말</text>'''

def child(c):
    return f'''<circle cx="60" cy="50" r="30" fill="#ffe0bd"/>
<path d="M30 46 Q30 18 60 18 Q90 18 90 46 Q80 30 60 30 Q40 30 30 46Z" fill="{INK}"/>
<circle cx="48" cy="50" r="9" fill="#fff" stroke="{c}" stroke-width="4"/><circle cx="72" cy="50" r="9" fill="#fff" stroke="{c}" stroke-width="4"/>
<circle cx="48" cy="50" r="3" fill="{INK}"/><circle cx="72" cy="50" r="3" fill="{INK}"/>
<path d="M28 52 Q20 52 22 64 Q28 66 30 58" fill="{c}"/><path d="M92 52 Q100 52 98 64 Q92 66 90 58" fill="{c}"/>
<path d="M50 66 Q60 74 70 66" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'''

def student(c):
    return f'''<circle cx="60" cy="44" r="26" fill="#ffe0bd"/>
<path d="M24 26 L60 10 L96 26 L60 42 Z" fill="{INK}"/><line x1="92" y1="28" x2="92" y2="46" stroke="#ffd166" stroke-width="3"/>
<circle cx="50" cy="48" r="3" fill="{INK}"/><circle cx="70" cy="48" r="3" fill="{INK}"/>
<rect x="28" y="76" width="64" height="34" rx="4" fill="{c}"/><line x1="60" y1="76" x2="60" y2="110" stroke="#fff" stroke-width="3"/>
<path d="M100 60 Q110 50 104 40" fill="none" stroke="{c}" stroke-width="3"/><circle cx="102" cy="36" r="3" fill="{c}"/>'''

def worker(c):
    return f'''<circle cx="60" cy="34" r="22" fill="#ffe0bd"/>
<circle cx="52" cy="34" r="3" fill="{INK}"/><circle cx="68" cy="34" r="3" fill="{INK}"/>
<path d="M52 44 Q60 50 68 44" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
<path d="M28 108 Q28 62 60 62 Q92 62 92 108 Z" fill="{c}"/>
<rect x="74" y="80" width="34" height="26" rx="4" fill="#8a5a2b"/><rect x="84" y="74" width="14" height="8" rx="2" fill="none" stroke="#8a5a2b" stroke-width="3"/>'''

def notebook(c):
    return f'''<rect x="26" y="12" width="70" height="96" rx="8" fill="{c}"/>
<rect x="38" y="12" width="6" height="96" fill="#fff" opacity=".5"/>
<rect x="52" y="30" width="34" height="6" rx="3" fill="#fff"/><rect x="52" y="46" width="34" height="6" rx="3" fill="#fff"/><rect x="52" y="62" width="24" height="6" rx="3" fill="#fff"/>
<path d="M80 86 L98 104 L104 98 L86 80 Z" fill="#ffd166"/>'''

def hand(c):
    return f'''<path d="M30 110 L30 60 Q30 52 38 52 Q46 52 46 60 L46 30 Q46 22 54 22 Q62 22 62 30 L62 26 Q62 18 70 18 Q78 18 78 26 L78 34 Q78 28 86 28 Q94 28 94 36 L94 80 Q94 110 64 110 Z" fill="{c}"/>
<path d="M14 64 Q22 56 30 64" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round"/>'''

def plug(c):
    return f'''<rect x="40" y="40" width="40" height="44" rx="8" fill="{c}"/>
<rect x="46" y="20" width="8" height="22" rx="3" fill="{INK}"/><rect x="66" y="20" width="8" height="22" rx="3" fill="{INK}"/>
<path d="M60 84 Q60 110 92 106" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round"/>'''

def shield(c):
    return f'''<path d="M60 10 L100 24 L100 58 Q100 92 60 110 Q20 92 20 58 L20 24 Z" fill="{c}"/>
<path d="M42 60 L56 74 L80 46" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'''

def stopsign(c):
    return f'''<path d="M40 10 L80 10 L110 40 L110 80 L80 110 L40 110 L10 80 L10 40 Z" fill="{c}"/>
<rect x="30" y="52" width="60" height="16" rx="4" fill="#fff"/>'''

def loop(c):
    return f'''<path d="M60 18 A42 42 0 1 1 22 74" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round"/>
<path d="M8 66 L22 80 L36 64" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="60" cy="60" r="14" fill="{c}" opacity=".5"/>'''

def calc(c):
    s = f'<rect x="24" y="10" width="72" height="100" rx="10" fill="{c}"/><rect x="34" y="20" width="52" height="22" rx="4" fill="#fff"/>'
    for r in range(3):
        for k in range(3):
            s += f'<rect x="{34+18*k}" y="{50+18*r}" width="14" height="14" rx="3" fill="#fff" opacity=".85"/>'
    return s

def doc(c):
    return f'''<path d="M26 10 L76 10 L96 30 L96 110 L26 110 Z" fill="#fff" stroke="{c}" stroke-width="6"/>
<path d="M76 10 L76 30 L96 30" fill="none" stroke="{c}" stroke-width="6"/>
<rect x="38" y="44" width="46" height="6" rx="3" fill="{c}"/><rect x="38" y="60" width="46" height="6" rx="3" fill="{c}"/><rect x="38" y="76" width="30" height="6" rx="3" fill="{c}"/>'''

def checkdoc(c):
    return doc(c) + f'<circle cx="92" cy="94" r="20" fill="#06d6a0"/><path d="M82 94 L90 102 L102 86" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/>'

def traffic(c):
    return f'''<rect x="36" y="6" width="48" height="108" rx="14" fill="{INK}"/>
<circle cx="60" cy="30" r="13" fill="#ef476f"/><circle cx="60" cy="60" r="13" fill="#ffd166"/><circle cx="60" cy="90" r="13" fill="#06d6a0"/>'''

def bulb(c):
    return f'''<circle cx="60" cy="48" r="32" fill="{c}"/>
<rect x="46" y="78" width="28" height="12" rx="3" fill="#9aa5b1"/><rect x="50" y="92" width="20" height="10" rx="3" fill="#9aa5b1"/>
<path d="M50 50 L56 60 L60 44 L64 60 L70 50" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'''

def team(c):
    s = ""
    for x, col in ((30, c), (60, "#ef476f"), (90, "#06d6a0")):
        s += f'<circle cx="{x}" cy="44" r="16" fill="{col}"/><path d="M{x-20} 100 Q{x-20} 66 {x} 66 Q{x+20} 66 {x+20} 100 Z" fill="{col}"/>'
    return s

def flag(c):
    return f'''<line x1="30" y1="12" x2="30" y2="110" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
<path d="M30 14 L98 14 L84 36 L98 58 L30 58 Z" fill="{c}"/>'''

ICONS = {k: v for k, v in globals().items() if callable(v) and k not in ("ICONS",)}

def svg(name, c, size=120):
    return f'<svg viewBox="0 0 120 120" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">{ICONS[name](c)}</svg>'
