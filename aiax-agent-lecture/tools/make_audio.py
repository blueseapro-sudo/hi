"""lecture/듣기/*.md 대본을 읽어 site/audio/ 에 회차별 mp3, 자막 시간표, 팟캐스트 피드를 만든다.

실행: python tools/make_audio.py          (필요: pip install edge-tts, ffmpeg)
대본 규칙: "H:" 진행자, "G:" 지니, "[쉼 n]" n초 쉼, "[종]" 장면 전환 종소리
"""
import asyncio, hashlib, json, os, re, ssl, subprocess, pathlib, datetime, email.utils
import edge_tts, edge_tts.communicate as _cm

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / 'lecture' / '듣기', ROOT / 'site' / 'audio'
CACHE = pathlib.Path(os.environ.get('AUDIO_CACHE', ROOT / '.audio_cache'))
SITE = os.environ.get('SITE_URL', 'https://aiax-agent-lecture.netlify.app')
VOICE = {'H': ('ko-KR-InJoonNeural', '+0%', '+0Hz'), 'G': ('ko-KR-SunHiNeural', '+4%', '+10Hz')}
GAP, SR = 0.32, 24000

ca = os.environ.get('SSL_CERT_FILE') or ('/root/.ccr/ca-bundle.crt' if os.path.exists('/root/.ccr/ca-bundle.crt') else None)
if ca: _cm._SSL_CTX = ssl.create_default_context(cafile=ca)
PROXY = os.environ.get('HTTPS_PROXY')

def run(*a): subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)

def parse(p):
    t = p.read_text(encoding='utf-8'); fm = {}
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    for l in m.group(1).splitlines():
        if ':' in l: k, v = l.split(':', 1); fm[k.strip()] = v.strip()
    items = []
    for l in t[m.end():].splitlines():
        l = l.strip()
        if re.match(r'^[HG]:', l): items.append(('say', l[0], l[2:].strip()))
        elif re.match(r'^\[쉼 (\d+(?:\.\d+)?)\]$', l): items.append(('rest', float(re.findall(r'[\d.]+', l)[0])))
        elif l == '[종]': items.append(('chime',))
    return fm, items

async def tts(who, text, sem):
    v, rate, pitch = VOICE[who]
    key = hashlib.sha1(f'{v}|{rate}|{pitch}|{text}'.encode()).hexdigest()[:16]
    mp3, wav = CACHE / f'{key}.mp3', CACHE / f'{key}.wav'
    if not wav.exists():
        async with sem:
            for attempt in range(4):
                try:
                    await edge_tts.Communicate(text, v, rate=rate, pitch=pitch, proxy=PROXY).save(str(mp3)); break
                except Exception:
                    if attempt == 3: raise
                    await asyncio.sleep(2 + attempt * 2)
        run('ffmpeg', '-y', '-i', str(mp3), '-ar', str(SR), '-ac', '1', str(wav))
    return wav

def silence(sec):
    p = CACHE / f'sil_{sec:.2f}.wav'
    if not p.exists(): run('ffmpeg', '-y', '-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=mono', '-t', f'{sec:.2f}', str(p))
    return p

def chime():
    p = CACHE / 'chime.wav'
    if not p.exists():
        run('ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=f=1046.5:d=0.9', '-f', 'lavfi', '-i', 'sine=f=1318.5:d=0.9',
            '-filter_complex', '[0]volume=0.22,afade=t=out:st=0.05:d=0.85[a];[1]adelay=180,volume=0.18,afade=t=out:st=0.25:d=0.65[b];[a][b]amix=inputs=2:duration=longest,apad=pad_dur=0.25',
            '-ar', str(SR), '-ac', '1', str(p))
    return p

async def episode(p, sem):
    fm, items = parse(p)
    ep = int(fm['episode']); name = f'ep{ep:02d}'
    wavs = await asyncio.gather(*[tts(i[1], i[2], sem) for i in items if i[0] == 'say'])
    seq, cues, t, k = [], [], 0.0, 0
    for i in items:
        if i[0] == 'say':
            w = wavs[k]; k += 1; d = dur(w)
            cues.append({'t': round(t, 2), 'who': i[1], 'text': i[2]})
            seq += [w, silence(GAP)]; t += d + GAP
        elif i[0] == 'rest': seq.append(silence(i[1])); t += i[1]
        else: c = chime(); seq.append(c); t += dur(c)
    lst = CACHE / f'{name}.txt'; lst.write_text(''.join(f"file '{s}'\n" for s in seq))
    OUT.mkdir(parents=True, exist_ok=True)
    mp3 = OUT / f'{name}.mp3'
    run('ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=9',
        '-ar', str(SR), '-ac', '1', '-b:a', '64k',
        '-metadata', f"title={fm['title']}", '-metadata', 'artist=AI 지니와 떠나는 여행', '-metadata', 'album=AI 이해부터 에이전트 개발까지',
        '-metadata', f'track={ep + 1}', str(mp3))
    return {'id': name, 'ep': ep, 'doc': fm.get('doc', ''), 'title': fm['title'], 'desc': fm.get('desc', ''),
            'src': f'audio/{name}.mp3', 'dur': round(dur(mp3), 1), 'bytes': mp3.stat().st_size, 'cues': cues}

def feed(eps):
    now = datetime.datetime(2026, 10, 27, 9, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    items = []
    for e in eps:
        pub = email.utils.format_datetime(now - datetime.timedelta(minutes=e['ep']))
        m, s = divmod(int(e['dur']), 60)
        items.append(f'''<item><title>{esc(e['title'])}</title><description>{esc(e['desc'])}</description>
<enclosure url="{SITE}/{e['src']}" length="{e['bytes']}" type="audio/mpeg"/><guid isPermaLink="false">aiax-{e['id']}</guid>
<pubDate>{pub}</pubDate><itunes:duration>{m:02d}:{s:02d}</itunes:duration><itunes:episode>{e['ep'] + 1}</itunes:episode><itunes:episodeType>full</itunes:episodeType><itunes:explicit>false</itunes:explicit></item>''')
    x = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel><title>AI 지니와 떠나는 여행</title><link>{SITE}/</link><language>ko</language>
<description>차에서 듣는 AI 강의. AI의 역사부터 에이전트에게 일을 맡기는 법까지, 진행자와 지니의 대화로 듣습니다.</description>
<itunes:author>AI 이해부터 에이전트 개발까지</itunes:author><itunes:type>serial</itunes:type><itunes:explicit>false</itunes:explicit>
<itunes:image href="{SITE}/audio/cover.jpg"/><image><url>{SITE}/audio/cover.jpg</url><title>AI 지니와 떠나는 여행</title><link>{SITE}/</link></image>
<itunes:category text="Education"/>
{chr(10).join(items)}
</channel></rss>'''
    (OUT / 'feed.xml').write_text(x, encoding='utf-8')

async def main():
    CACHE.mkdir(exist_ok=True); sem = asyncio.Semaphore(6)
    eps = sorted([await episode(p, sem) for p in sorted(SRC.glob('AIAX_듣기_*.md'))], key=lambda e: e['ep'])
    (OUT / 'episodes.json').write_text(json.dumps(eps, ensure_ascii=False), encoding='utf-8')
    feed(eps)
    for e in eps: print(f"{e['id']}  {int(e['dur'])//60}:{int(e['dur'])%60:02d}  {e['bytes']//1024}KB  {e['title']}")
    print('total', round(sum(e['dur'] for e in eps) / 60, 1), 'min')

asyncio.run(main())
