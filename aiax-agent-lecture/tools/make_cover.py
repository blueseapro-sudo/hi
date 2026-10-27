"""팟캐스트 표지 site/audio/cover.png (3000x3000) 를 만든다."""
import asyncio, pathlib, re
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'tools' / 'infographic' / 'make2.py').read_text(encoding='utf-8')
ns = {}; exec(re.search(r'^def genie\(.*?(?=^def )', src, re.S | re.M).group(0), ns)
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1000px;height:1000px;background:linear-gradient(150deg,#1d3f99 0%,#0c1a45 70%);font-family:'Noto Sans CJK KR',sans-serif;color:#fff;position:relative;overflow:hidden}}
.road{{position:absolute;left:-60px;right:-60px;bottom:120px;height:120px;border-top:14px dashed rgba(255,255,255,.35);border-radius:50% 50% 0 0}}
.ring{{position:absolute;border-radius:50%;border:2px solid rgba(255,255,255,.08)}}
.g{{position:absolute;right:70px;bottom:150px}}
.t{{position:absolute;left:80px;top:110px;right:80px}}
.k{{display:inline-block;background:#f6b419;color:#0c1a45;font-weight:900;font-size:36px;border-radius:14px;padding:8px 22px}}
h1{{font-weight:900;font-size:118px;line-height:1.08;letter-spacing:-3px;margin-top:34px}}
p{{font-size:40px;margin-top:26px;opacity:.88}}
.b{{position:absolute;left:80px;bottom:70px;font-size:30px;opacity:.75}}
</style></head><body>
<div class="ring" style="width:900px;height:900px;right:-380px;top:-380px"></div><div class="ring" style="width:600px;height:600px;right:-230px;top:-230px"></div>
<div class="road"></div>
<div class="t"><span class="k">차에서 듣는 AI 강의</span><h1>AI 지니와<br>떠나는 여행</h1><p>역사부터 에이전트까지 9편</p></div>
<div class="g">{ns['genie'](330, point=True)}</div>
<div class="b">AI 이해부터 에이전트 개발까지</div>
</body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1000, 'height': 1000}, device_scale_factor=3)
        await pg.set_content(html); await pg.wait_for_timeout(300)
        out = ROOT / 'site' / 'audio' / 'cover.png'; await pg.screenshot(path=str(out)); await b.close()
        from PIL import Image; i = Image.open(out).convert('RGB'); i.save(out.with_suffix('.jpg'), quality=88); i.resize((512, 512), Image.LANCZOS).save(out.parent / 'cover-512.jpg', quality=86); out.unlink(); print('cover.jpg, cover-512.jpg')
asyncio.run(main())
