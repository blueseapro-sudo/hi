import asyncio, sys, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
U = 'file://' + str(ROOT / 'site' / 'index.html')
OUT = ROOT / 'site' / 'pdf'; OUT.mkdir(exist_ok=True)
FOOT = '<div style="font-size:8px;width:100%;text-align:center;color:#888;font-family:sans-serif">AI 이해부터 에이전트 개발까지 · <span class="pageNumber"></span> / <span class="totalPages"></span></div>'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1100,'height':1400})
        await pg.goto(U+'#p00'); await pg.wait_for_timeout(2500)
        ids = await pg.evaluate('AIAX.docs')
        opt = dict(format='A4', print_background=True, margin={'top':'14mm','bottom':'16mm','left':'14mm','right':'14mm'}, display_header_footer=True, header_template='<div></div>', footer_template=FOOT)
        await pg.emulate_media(media='print')
        for i in ids:
            await pg.evaluate(f"location.hash='{i}'"); await pg.wait_for_timeout(1800)
            await pg.pdf(path=str(OUT/f'aiax_{i}.pdf'), **opt); print(i)
        await pg.evaluate('AIAX.renderAll()'); await pg.wait_for_timeout(6000)
        await pg.pdf(path=str(OUT/'aiax_all.pdf'), **opt); print('all')
        await b.close()
asyncio.run(main())
