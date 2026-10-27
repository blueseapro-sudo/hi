"""lecture/*.md 를 읽어 site/index.html 을 만든다.  실행: python tools/build.py"""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / 'lecture', ROOT / 'site'
docs = []
for i, p in enumerate(sorted(SRC.glob('AIAX_*.md'))):
    t = p.read_text(encoding='utf-8'); fm = {}
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if m:
        for l in m.group(1).splitlines():
            if ':' in l: k, v = l.split(':', 1); fm[k.strip()] = v.strip().strip('"')
    h1 = re.search(r'^# (.+)$', t, re.M); n = re.search(r'_(\d+)_', p.name)
    docs.append({'id': 'p' + n.group(1), 'file': p.name, 'title': fm.get('title') or h1.group(1),
                 'navTitle': fm.get('nav') or h1.group(1), 'part': fm.get('part', '본강'),
                 'order': float(fm.get('order', i)), 'time': fm.get('time', ''), 'md': t})
files = {'kit': 'kit/agent-lab.zip', 'pdfAll': 'pdf/aiax_all.pdf', 'pdf': {d['id']: f"pdf/aiax_{d['id']}.pdf" for d in docs}}
course = {'title': 'AI 이해부터 에이전트 개발까지', 'start': '09:00', 'files': files}
AJ = OUT / 'audio' / 'episodes.json'
if AJ.exists(): course['audio'] = json.loads(AJ.read_text(encoding='utf-8'))
data = json.dumps({'course': course, 'docs': docs}, ensure_ascii=False).replace('</', '<\\/')
e = (ROOT / 'tools' / 'engine.html').read_text(encoding='utf-8')
e = re.sub(r'(<script type="application/json" id="course-data">).*?(</script>)', lambda m: m.group(1) + data + m.group(2), e, count=1, flags=re.S)
e = re.sub(r'<title>.*?</title>', '<title>AI 에이전트 강의실</title>', e, count=1)
e = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + 'AI 역사·용어·모델 연표부터 Claude Code 에이전트 실습까지', e, count=1)
head = '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><link rel="alternate" type="application/rss+xml" title="AI 지니와 떠나는 여행" href="audio/feed.xml"><meta name="theme-color" content="#0c1a45">'
OUT.mkdir(exist_ok=True)
(OUT / 'index.html').write_text(head + '</head><body>' + e + '</body></html>', encoding='utf-8')
print(len(docs), 'docs ->', OUT / 'index.html')
