import asyncio, sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from icons import ICONS
from playwright.async_api import async_playwright

OUT = pathlib.Path(__file__).resolve().parents[2] / "lecture" / "images"; OUT.mkdir(parents=True, exist_ok=True)
W, H = 1920, 1080
INK, PAPER, TEAL, GOLD, RED, LEAF, SKY, PLUM = "#1B2A4A", "#F3F8FC", "#0FA3B1", "#F6B419", "#E2483D", "#2FA66B", "#4C8DDE", "#7B5CD6"
e = html.escape

def ico(name, c, s=120):
    return f'<svg viewBox="0 0 120 120" width="{s}" height="{s}">{ICONS[name](c)}</svg>'

def disc(name, c, s=150, ring=None):
    ring = ring or c
    return f'''<div class="disc" style="width:{s}px;height:{s}px;border-color:{ring};box-shadow:0 10px 0 {ring}33">{ico(name, c, int(s*.62))}</div>'''

def genie(s=260, mood="happy", point=True):
    arm = ('<path d="M150 150 Q190 120 200 84" stroke="#39C0D0" stroke-width="18" stroke-linecap="round" fill="none"/>'
           '<circle cx="201" cy="78" r="12" fill="#39C0D0"/><rect x="176" y="112" width="18" height="10" rx="4" fill="#F6B419" transform="rotate(-50 185 117)"/>') if point else \
          '<path d="M150 160 Q178 176 170 200" stroke="#39C0D0" stroke-width="18" stroke-linecap="round" fill="none"/>'
    return f'''<svg viewBox="0 0 230 320" width="{s}" height="{int(s*320/230)}">
<defs><linearGradient id="tl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#39C0D0"/><stop offset="1" stop-color="#39C0D0" stop-opacity=".15"/></linearGradient></defs>
<path d="M78 196 Q60 250 96 272 Q130 292 120 312 Q170 290 140 250 Q118 222 150 196 Z" fill="url(#tl)"/>
<path d="M70 150 Q70 128 92 126 L138 126 Q160 128 160 150 L156 204 Q115 222 74 204 Z" fill="#7B5CD6"/>
<path d="M92 126 L115 176 L138 126" fill="#39C0D0"/>
<path d="M80 150 Q48 168 58 196" stroke="#39C0D0" stroke-width="18" stroke-linecap="round" fill="none"/>
<rect x="50" y="172" width="18" height="10" rx="4" fill="#F6B419" transform="rotate(70 59 177)"/>
{arm}
<circle cx="115" cy="86" r="50" fill="#39C0D0"/>
<path d="M115 20 Q100 36 115 42 Q130 36 115 20 Z" fill="#1B2A4A"/>
<path d="M118 30 Q150 18 160 40 Q150 30 128 38" fill="#1B2A4A"/>
<circle cx="66" cy="92" r="8" fill="none" stroke="#F6B419" stroke-width="4"/>
<path d="M90 82 Q98 72 106 82" stroke="#1B2A4A" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M124 82 Q132 72 140 82" stroke="#1B2A4A" stroke-width="5" fill="none" stroke-linecap="round"/>
<circle cx="88" cy="100" r="7" fill="#FF8FA3" opacity=".7"/><circle cx="142" cy="100" r="7" fill="#FF8FA3" opacity=".7"/>
<path d="M100 104 Q115 120 130 104" fill="#1B2A4A"/>
</svg>'''

def bubble(text, w=520, tail="left"):
    return f'<div class="bubble {tail}" style="width:{w}px">{text}</div>'

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:{PAPER};font-family:'Noto Sans CJK KR',sans-serif;color:{INK};word-break:keep-all;position:relative}}
.bgc{{position:absolute;border-radius:50%;background:#E3EEF8}}
.hd{{position:absolute;left:80px;top:60px;right:80px}}
.chip{{display:inline-block;background:{INK};color:#fff;font-weight:700;font-size:26px;padding:6px 20px;border-radius:12px;margin-bottom:14px}}
.hd h1{{font-weight:900;font-size:78px;line-height:1.05;letter-spacing:-2px}}
.hd p{{font-size:30px;color:#4A5A78;margin-top:14px}}
.abs{{position:absolute}}
.disc{{border-radius:50%;background:#fff;border:6px solid;display:flex;align-items:center;justify-content:center}}
.t{{font-weight:900;font-size:34px;line-height:1.2}}
.d{{font-size:25px;line-height:1.4;color:#33415E;margin-top:6px}}
.ex{{display:inline-block;margin-top:10px;font-size:22px;line-height:1.35;background:#fff;border-radius:10px;padding:6px 12px;color:{INK}}}
.yr{{font-weight:900;font-size:26px;color:#fff;border-radius:22px;padding:4px 16px;display:inline-block}}
.bubble{{position:absolute;background:#fff;border:4px solid {INK};border-radius:28px;padding:22px 28px;font-size:32px;font-weight:700;line-height:1.4;box-shadow:0 8px 0 {INK}22}}
.bubble:after{{content:"";position:absolute;bottom:26px;width:0;height:0;border-top:16px solid transparent;border-bottom:16px solid transparent}}
.bubble.left:after{{left:-26px;border-right:24px solid {INK}}}
.bubble.right:after{{right:-26px;border-left:24px solid {INK}}}
.bubble.down:after{{bottom:-26px;right:80px;border-top:24px solid {INK};border-left:16px solid transparent;border-right:16px solid transparent;border-bottom:0}}
.bubble b{{color:{TEAL}}}
.ctr{{text-align:center}}
.note{{font-size:20px;color:#6A7894}}
"""

def page(body, bg=""):
    circles = '<div class="bgc" style="width:900px;height:900px;right:-300px;top:-420px"></div><div class="bgc" style="width:520px;height:520px;left:-200px;bottom:-260px"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{circles}{bg}{body}</body></html>'

def head(chip, title, sub):
    return f'<div class="hd"><span class="chip">{e(chip)}</span><h1>{e(title)}</h1><p>{e(sub)}</p></div>'

def at(x, y, w, inner, cls="", style=""):
    return f'<div class="abs {cls}" style="left:{x}px;top:{y}px;width:{w}px;{style}">{inner}</div>'

# ---------- journey (road with stops) ----------
def journey(stops, y0=600, amp=70, x0=150, x1=1500, extra_svg=""):
    n = len(stops); xs = [x0 + (x1-x0)*i/(n-1) for i in range(n)]
    ys = [y0 + (amp if i % 2 else -amp) for i in range(n)]
    d = f"M{xs[0]-80} {ys[0]} " + " ".join(f"S{(xs[i-1]+xs[i])/2} {ys[i]} {xs[i]} {ys[i]}" for i in range(1, n))
    svg = f'''<svg class="abs" style="left:0;top:0" width="{W}" height="{H}">{extra_svg}
<path d="{d}" stroke="#D3E1EE" stroke-width="54" fill="none" stroke-linecap="round"/>
<path d="{d}" stroke="#fff" stroke-width="6" fill="none" stroke-dasharray="22 20"/></svg>'''
    out = svg
    for i, (icon, col, yr, t, desc) in enumerate(stops):
        x, y = xs[i], ys[i]
        out += at(x-70, y-70, 140, disc(icon, col, 140))
        up = i % 2 == 0
        ty = y - 330 if up else y + 90
        out += at(x-140, ty, 280, f'<div class="ctr"><span class="yr" style="background:{col}">{e(yr)}</span><div class="t" style="margin-top:10px">{e(t)}</div><div class="d">{e(desc)}</div></div>',
                  style=f"height:240px;display:flex;flex-direction:column;justify-content:{'flex-end' if up else 'flex-start'}")
    return out

SHEETS = []
def sheet(f):
    SHEETS.append(f); return f

@sheet
def s00():
    stops = [("lamp",GOLD,"1강","지니가 태어나요","AI가 자라 온 70년"),
             ("wish",RED,"2강","소원 비는 법","자세히 말하면 잘 들어줘요"),
             ("student",SKY,"3강","지니가 자라요","해마다 더 똑똑해져요"),
             ("notebook",PLUM,"4강","업무 수첩","우리 규칙을 적어 줘요"),
             ("hand",TEAL,"5강","손발과 약속","도구를 쓰고 약속을 지켜요"),
             ("team",LEAF,"6강","지니 팀","나눠서 일하면 실수가 줄어요"),
             ("traffic",INK,"활용편","무엇을 맡길까","신호등으로 정해요")]
    b = head("전체 지도", "AI 지니와 떠나는 여행", "일곱 정거장을 지나면 내 일을 AI에게 맡길 수 있어요")
    b += journey(stops, y0=640, amp=60, x0=170, x1=1330)
    b += at(1600, 680, 280, genie(230))
    b += bubble("잘 부탁하고, <b>꼭 확인</b>하면 내가 도와줄게!", 380, "down").replace('class="bubble down"', 'class="bubble down" style="left:1510px;top:440px;width:370px"', 1)
    return "aiax_ig_00_overview", b

@sheet
def s01():
    snow = f'<rect x="447" y="300" width="220" height="650" rx="40" fill="#DCEAF7"/><text x="557" y="995" text-anchor="middle" font-size="26" font-weight="700" fill="{SKY}" font-family="Noto Sans CJK KR">AI의 겨울</text>'
    stops = [("question",SKY,"1950","궁금해요","기계도 생각할 수 있을까?"),
             ("tag",PLUM,"1956","이름이 생겼어요","인공지능, AI라고 불러요"),
             ("snow",SKY,"1970~80","추운 겨울","잘 안 돼서 연구가 멈췄어요"),
             ("photos",LEAF,"1990~","보고 배워요","사진을 많이 보고 스스로 알아내요"),
             ("board",GOLD,"2016","바둑을 이겼어요","알파고가 이세돌 9단을 이겼어요"),
             ("bubble",RED,"2022","말을 해요","AI와 이야기를 나눠요"),
             ("robot",TEAL,"지금","일을 해요","시키면 혼자 끝까지 해요")]
    b = head("1강", "AI는 이렇게 자랐어요", "생각하는 기계를 꿈꾼 지 70년, 쉬었다가 다시 달렸어요")
    b += journey(stops, y0=650, amp=60, x0=170, x1=1330, extra_svg=snow)
    b += at(1600, 690, 280, genie(230))
    b += bubble("겨울에도 포기하지 않은 사람들 덕분에 <b>봄이 왔어요</b>", 380, "down").replace('class="bubble down"', 'class="bubble down" style="left:1510px;top:430px;width:370px"', 1)
    return "aiax_ig_01_history", b

@sheet
def s02():
    words = [("magnifier",SKY,"리터러시","AI가 틀리면 알아채는 힘","\"고래가 하늘을 날아요?\" 이상한데!"),
             ("wish",RED,"프롬프트","AI에게 하는 부탁","\"과자 줘\"보다 \"초코 과자 3개 줘\""),
             ("brain",PLUM,"모델","AI의 머리","ChatGPT는 가게, GPT-5는 요리사"),
             ("blocks",LEAF,"바이브 코딩","말하면 AI가 만들어요","\"빨간 지붕 집 지어줘\""),
             ("armleg",GOLD,"피지컬 AI","몸이 있는 AI","로봇, 드론, 자율주행차"),
             ("ladder",RED,"격차","쓰는 사람과 못 쓰는 사람의 차이","요술 연필이 있는 친구와 없는 친구"),
             ("spiral",INK,"특이점","AI가 사람보다 똑똑해지는 날","아직 안 왔어요. 어른들도 몰라요"),
             ("spark",GOLD,"반짝 단어","잠깐 유행하고 사라진 말","프롬프트 엔지니어, 메타버스")]
    b = head("2강", "AI 말 그림사전", "어려운 말도 그림으로 보면 쉬워요")
    cw, chh = 400, 330
    for i, (ic, col, t, dsc, ex) in enumerate(words):
        r, c = divmod(i, 4)
        x, y = 80 + c*(cw+40), 300 + r*(chh+40)
        tint = col + "18"
        b += at(x, y, cw, f'''<div style="height:{chh}px;border-radius:30px;background:linear-gradient({tint},{tint}),#fff;padding:26px 26px 22px 26px;position:relative">
<div style="display:flex;gap:18px;align-items:center">{disc(ic,col,110)}<div><div class="t" style="font-size:38px">{e(t)}</div></div></div>
<div class="d" style="margin-top:16px;font-size:27px;font-weight:700;color:{INK}">{e(dsc)}</div>
<div class="ex"><span style="color:{col};font-weight:900">예</span>&nbsp; {e(ex)}</div></div>''')
    return "aiax_ig_02_words", b

@sheet
def s03():
    steps = [("baby",RED,"1막","2022~2023","말을 배운 아기","대화를 해요","ChatGPT, GPT-4"),
             ("child",SKY,"2막","2024","눈과 귀가 생긴 어린이","보고 듣고 말해요","GPT-4o, Claude 3.5"),
             ("student",PLUM,"3막","2025","생각하는 학생","풀기 전에 생각하고 코딩해요","o1 이후, Claude 4, GPT-5"),
             ("worker",LEAF,"4막","2026","심부름하는 비서","혼자 계획하고 끝내요","Claude 5.5, GPT-6")]
    b = head("3강", "AI가 쑥쑥 자랐어요", "2022년부터 지금까지 네 번 모습이 바뀌었어요")
    base = 960; stepw = 360
    svg = f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}">'
    for i in range(4):
        x = 100 + i*(stepw+20); h = 230 + i*90
        svg += f'<rect x="{x}" y="{base-h}" width="{stepw}" height="{h}" rx="22" fill="{steps[i][1]}"/>'
        svg += f'<text x="{x+30}" y="{base-h+56}" font-size="40" font-weight="900" fill="#fff" font-family="Noto Sans CJK KR">{steps[i][2]}</text>'
        svg += f'<text x="{x+stepw-30}" y="{base-h+54}" font-size="28" font-weight="700" fill="#fff" text-anchor="end" font-family="Noto Sans CJK KR">{steps[i][3]}</text>'
    svg += f'<path d="M140 {base+40} L{100+4*(stepw+20)-40} {base+40}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M{100+4*(stepw+20)-60} {base+26} L{100+4*(stepw+20)-34} {base+40} L{100+4*(stepw+20)-60} {base+54}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    svg += f'<text x="140" y="{base+90}" font-size="24" fill="#4A5A78" font-family="Noto Sans CJK KR">시간이 흐를수록 할 수 있는 일이 늘어나요</text></svg>'
    b += svg
    for i, (ic, col, act, yr, who, can, ex) in enumerate(steps):
        x = 100 + i*(stepw+20); h = 230 + i*90; top = base - h
        b += at(x+12, top + 76, stepw-24, f'<div style="color:#fff"><div class="t" style="font-size:32px">{e(who)}</div><div style="font-size:24px;margin-top:4px;opacity:.95">{e(can)}</div></div>')
        b += at(x + stepw/2 - 75, top - 175, 150, disc(ic, col, 150))
        b += at(x+12, top + 168, stepw-24, f'<div style="font-size:20px;color:#fff;opacity:.85">{e(ex)}</div>')
    b += at(1690, 60, 200, genie(150, point=False))
    b += bubble("이름은 매달 바뀌어요.<br><b>지금 몇 막인지</b>만 기억해요", 560, "right").replace('class="bubble right"', 'class="bubble right" style="left:1090px;top:80px;width:560px"', 1)
    return "aiax_ig_03_timeline", b

@sheet
def s04():
    b = head("4강", "지니에게 일을 맡기는 법", "에이전트는 시키면 스스로 계획하고 끝까지 해내는 지니예요")
    cx, cy, R = 470, 660, 230
    nodes = [("wish",GOLD,"부탁 받기"),("flag",PLUM,"계획 세우기"),("hand",TEAL,"도구로 하기"),("checkdoc",LEAF,"확인하기")]
    import math
    svg = f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}"><circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#D3E1EE" stroke-width="34"/>'
    for k in range(4):
        a = -math.pi/2 + k*math.pi/2 + math.pi/4
        ax, ay = cx + R*math.cos(a), cy + R*math.sin(a)
        rot = math.degrees(a) + 90
        svg += f'<path d="M-14 -16 L14 0 L-14 16 Z" fill="{INK}" transform="translate({ax} {ay}) rotate({rot})"/>'
    svg += '</svg>'
    b += svg
    for k, (ic, col, t) in enumerate(nodes):
        a = -math.pi/2 + k*math.pi/2
        x, y = cx + R*math.cos(a), cy + R*math.sin(a)
        b += at(x-60, y-60, 120, disc(ic, col, 120))
        lx = {0: x-110, 1: x+70, 2: x-110, 3: x-290}[k]; ly = {0: y-110, 1: y-22, 2: y+68, 3: y-22}[k]
        b += at(lx, ly, 220, f'<div class="t" style="font-size:30px;text-align:{"left" if k==1 else ("right" if k==3 else "center")}">{e(t)}</div>')
    b += at(cx-80, cy-110, 160, genie(150, point=False))
    # wish card
    rows = [("무엇을", GOLD, "월별 예산 보고서 1장"),
            ("무엇으로", SKY, "예산 엑셀 파일"),
            ("하지 말 것", RED, "원본 파일은 고치지 않기"),
            ("다 됐나요?", LEAF, "합계가 원본과 같은지 확인")]
    card = f'<div style="background:#fff;border:5px solid {INK};border-radius:30px;padding:30px 34px;box-shadow:12px 12px 0 {INK}1f"><div class="t" style="font-size:40px">소원 카드</div><div class="d" style="margin-bottom:14px">이 네 칸을 채워서 부탁해요</div>'
    for t, col, v in rows:
        card += f'<div style="display:flex;align-items:center;gap:18px;padding:16px 0;border-top:3px dashed #D3E1EE"><span style="background:{col};color:#fff;font-weight:900;font-size:26px;border-radius:14px;padding:6px 14px;min-width:170px;text-align:center">{e(t)}</span><span style="font-size:29px;font-weight:700">{e(v)}</span></div>'
    card += '</div>'
    b += at(1000, 290, 840, card)
    tools = [("notebook",PLUM,"업무 수첩","우리 규칙 적어 두기"),("stopsign",RED,"멈춤 표지","위험한 일 못 하게"),("flag",TEAL,"먼저 계획","큰일은 계획부터")]
    row = '<div style="display:flex;gap:18px">'
    for ic, col, t, dsc in tools:
        row += f'<div style="flex:1;display:flex;gap:12px;align-items:center;background:{col}18;border-radius:22px;padding:14px">{ico(ic,col,64)}<div><div style="font-weight:900;font-size:26px">{e(t)}</div><div style="font-size:21px;color:#33415E">{e(dsc)}</div></div></div>'
    row += '</div>'
    b += at(1000, 900, 840, row)
    return "aiax_ig_04_agent", b

@sheet
def s05():
    b = head("5강", "지니의 손발, 수첩, 약속", "MCP, 스킬, 훅은 지니가 일을 더 잘하게 도와줘요")
    gx, gy = 960, 560
    b += at(gx-115, gy-190, 230, genie(230, point=False))
    parts = [(240, 300, "plug", SKY, "MCP", "손과 발", "밖에 있는 자료를 가져와요", "공유폴더의 엑셀 읽기", "지니가 필요할 때 써요"),
             (1290, 300, "notebook", PLUM, "스킬", "업무 수첩", "자주 하는 일의 순서를 적어 둬요", "매주 보고서 만드는 순서", "지니가 골라서 꺼내요"),
             (765, 790, "shield", RED, "훅", "꼭 지키는 약속", "정해진 때가 되면 무조건 해요", "원본을 지우려 하면 멈춤", "언제나 자동으로 해요")]
    svg = f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}">'
    for (x, y, *_r), (tx, ty) in zip(parts, [(gx-80, gy-50), (gx+80, gy-50), (gx, gy+150)]):
        sx, sy = (x+390, y+150) if x < 900 and y < 800 else ((x, y+150) if y < 800 else (x+195, y))
        svg += f'<path d="M{sx} {sy} Q{(sx+tx)/2} {sy} {tx} {ty}" stroke="{INK}" stroke-width="5" fill="none" stroke-dasharray="4 12" stroke-linecap="round"/><circle cx="{tx}" cy="{ty}" r="10" fill="{INK}"/>'
    svg += '</svg>'
    b += svg
    for x, y, ic, col, name, nick, dsc, ex, who in parts:
        w = 390
        inner = f'''<div style="background:#fff;border-radius:30px;border:5px solid {col};padding:22px 24px;box-shadow:0 10px 0 {col}33">
<div style="display:flex;gap:16px;align-items:center">{ico(ic,col,84)}<div><div style="font-size:24px;font-weight:700;color:{col}">{e(name)}</div><div class="t" style="font-size:38px">{e(nick)}</div></div></div>
<div class="d" style="font-size:25px">{e(dsc)}</div>
<div class="ex" style="background:{col}18"><b style="color:{col}">예</b>&nbsp; {e(ex)}</div>
<div style="margin-top:10px;font-size:21px;color:#6A7894">{e(who)}</div></div>'''
        b += at(x, y, w, inner)
    return "aiax_ig_05_tools", b

@sheet
def s06():
    b = head("6강", "지니 팀으로 일해요", "한 명이 다 하지 않고 나눠서 하면 틀린 것을 찾을 수 있어요")
    stations = [(90, "doc", INK, "자료", "가짜 출동 실적 엑셀"),
                (470, "calc", SKY, "계산 지니", "숫자를 세고 표를 만들어요"),
                (850, "notebook", PLUM, "작성 지니", "수첩 순서대로 보고서를 써요"),
                (1230, "magnifier", RED, "검토 지니", "틀린 곳만 찾아요. 고치지는 않아요"),
                (1610, "checkdoc", LEAF, "완성", "확인이 끝난 보고서")]
    y = 560
    svg = f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}"><rect x="60" y="{y+70}" width="1800" height="40" rx="20" fill="#D3E1EE"/>'
    for i in range(30):
        svg += f'<circle cx="{90+i*61}" cy="{y+90}" r="8" fill="#fff"/>'
    svg += f'<path d="M1300 {y-40} Q1110 {y-170} 930 {y-40}" stroke="{RED}" stroke-width="6" fill="none" stroke-dasharray="14 10"/><path d="M942 {y-62} L926 {y-36} L956 {y-36}" fill="{RED}"/>'
    svg += f'<text x="1115" y="{y-150}" text-anchor="middle" font-size="26" font-weight="900" fill="{RED}" font-family="Noto Sans CJK KR">틀렸어요! 다시 써 주세요</text></svg>'
    b += svg
    for x, ic, col, t, dsc in stations:
        b += at(x+60, y-60, 160, disc(ic, col, 160))
        b += at(x, y+140, 280, f'<div class="ctr"><div class="t" style="color:{col}">{e(t)}</div><div class="d">{e(dsc)}</div></div>')
    found = f'<div style="background:#fff;border:4px solid {RED};border-radius:20px;padding:14px 18px;font-size:24px;line-height:1.45"><b style="color:{RED}">검토 지니가 찾았어요</b><br>마센터 합계 30 → 다시 세면 27</div>'
    b += at(1230, 880, 360, found)
    b += at(150, 880, 230, genie(150, point=False), style="")
    b += bubble("쓴 지니와 <b>검사하는 지니</b>는 따로!", 520, "left").replace('class="bubble left"', 'class="bubble left" style="left:330px;top:900px;width:560px"', 1)
    return "aiax_ig_06_team", b

@sheet
def s95():
    b = head("활용편", "무엇을 맡길까? 신호등에게 물어봐요", "내 일을 AI에게 맡기기 전에 두 가지만 확인해요")
    q1 = f'<div style="background:#fff;border:5px solid {INK};border-radius:26px;padding:20px 26px"><div style="font-size:22px;color:#6A7894;font-weight:700">질문 1</div><div class="t" style="font-size:34px">비밀 자료나 개인정보가 들어가나요?</div></div>'
    q2 = f'<div style="background:#fff;border:5px solid {INK};border-radius:26px;padding:20px 26px"><div style="font-size:22px;color:#6A7894;font-weight:700">질문 2</div><div class="t" style="font-size:34px">결과가 맞는지 내가 확인할 수 있나요?</div></div>'
    b += at(80, 300, 560, q1)
    b += at(80, 540, 560, q2)
    svg = f'''<svg class="abs" style="left:0;top:0" width="{W}" height="{H}">
<path d="M640 370 L760 370" stroke="{RED}" stroke-width="8"/><path d="M752 354 L780 370 L752 386Z" fill="{RED}"/>
<text x="700" y="350" text-anchor="middle" font-size="26" font-weight="900" fill="{RED}" font-family="Noto Sans CJK KR">예</text>
<path d="M360 470 L360 512" stroke="{LEAF}" stroke-width="8"/><path d="M344 508 L360 532 L376 508Z" fill="{LEAF}"/>
<text x="384" y="508" font-size="26" font-weight="900" fill="{LEAF}" font-family="Noto Sans CJK KR">아니오</text>
<path d="M640 620 L760 620" stroke="{GOLD}" stroke-width="8"/><path d="M752 604 L780 620 L752 636Z" fill="{GOLD}"/>
<text x="700" y="600" text-anchor="middle" font-size="26" font-weight="900" fill="#B07F00" font-family="Noto Sans CJK KR">아니오</text>
<path d="M360 712 L360 890 L760 890" stroke="{LEAF}" stroke-width="8" fill="none"/><path d="M752 874 L780 890 L752 906Z" fill="{LEAF}"/>
<text x="384" y="810" font-size="26" font-weight="900" fill="{LEAF}" font-family="Noto Sans CJK KR">예</text></svg>'''
    b += svg
    def light(col, on):
        cols = [RED, GOLD, LEAF]
        return '<div style="background:#1B2A4A;border-radius:22px;padding:10px 8px;display:flex;flex-direction:column;gap:8px;width:62px">' + "".join(f'<span style="width:46px;height:46px;border-radius:50%;background:{c if c==col else "#3A4A6A"}"></span>' for c in cols) + '</div>'
    def outcome(col, title, dsc, extra=""):
        return f'<div style="display:flex;gap:22px;align-items:center;background:{col}1c;border-radius:28px;padding:18px 24px">{light(col, True)}<div style="flex:1"><div class="t" style="font-size:36px">{e(title)}</div><div class="d" style="font-size:25px">{e(dsc)}</div>{extra}</div></div>'
    b += at(790, 290, 1050, outcome(RED, "빨간불: 멈춰요", "AI에 넣지 않아요. 지울 건 지우고, 먼저 허락을 받아요"))
    b += at(790, 530, 1050, outcome(GOLD, "노란불: 사람이 정해요", "AI 답은 참고만 하고, 결정은 내가 해요"))
    lv = "".join(f'<div style="flex:1;background:#fff;border-radius:18px;padding:10px 14px"><div style="font-weight:900;font-size:23px;color:{LEAF}">{e(a)}</div><div style="font-size:21px;line-height:1.35">{e(c)}</div></div>' for a, c in [("가끔 하는 일","그냥 잘 물어봐요"),("매주 하는 일","업무 수첩(스킬)"),("여러 단계 일","지니 팀")])
    b += at(790, 770, 1050, outcome(LEAF, "초록불: 맡겨요", "가장 쉬운 방법부터 골라요", f'<div style="display:flex;gap:12px;margin-top:12px">{lv}</div>'))
    return "aiax_ig_95_apply", b

async def main():
    only = set(sys.argv[1:])
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1.25)
        for f in SHEETS:
            name, body = f()
            if only and name not in only: continue
            await pg.set_content(page(body)); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT/(name+".png")))
            print(name)
        await br.close()
asyncio.run(main())
