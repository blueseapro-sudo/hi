# AI 이해부터 에이전트 개발까지

소방공무원 교육생 대상 AI·AX 강의 교재 (3시간 15분). AI 역사, 핵심 용어, 2022~2026 모델 연표, Claude Code 에이전트 실습(CLAUDE.md, MCP, 스킬, 훅, 멀티에이전트), 활용편으로 구성.

## 폴더

| 폴더 | 내용 |
|---|---|
| `lecture/` | 옵시디언 md 원본 11개와 인포그래픽(`images/`) |
| `lecture/듣기/` | 차에서 듣기용 라디오 대본 9편 (진행자·지니 대화) |
| `site/` | 배포용 강의 사이트 (`index.html`, PDF, 실습파일) |
| `agent-lab/` | 4~6강 실습 폴더 (가짜 데이터, CLAUDE.md, 훅, 스킬, 서브에이전트) |
| `tools/` | 사이트·PDF·인포그래픽을 다시 만드는 스크립트 |

## 사이트 기능

목차 접기, 실습파일 받기, 타이머(크게 보기, 강의 시작 시각), PDF 다운로드(전체·장별), 인쇄, 발표 모드(가로로), 어둡게, 확대·축소, 내 상황별 예시, 진행률, 장 안 차례, 코드 복사 버튼, 퀴즈, 아이디어 설계기.

## 차에서 듣기

- 사이트 위쪽 "차에서 듣기" 또는 `/#listen`: 9편 약 40분, 큰 버튼, 15초 뒤로·30초 앞으로, 속도, 다음 편 이어 듣기, 이어 듣기 위치 기억, 자막
- 잠금 화면·블루투스·핸들 버튼으로 재생·일시정지·다음 편 (Media Session)
- 팟캐스트 피드: `/audio/feed.xml` (아이폰 팟캐스트 앱의 "URL로 프로그램 팔로우" 등에 등록)

## 다시 만들기

```bash
pip install playwright
python tools/build.py          # lecture/*.md -> site/index.html
cp lecture/images/*.png site/images/
python tools/mkpdf.py          # site/pdf/*.pdf (Chromium 필요)
pip install edge-tts
python tools/make_audio.py     # lecture/듣기/*.md -> site/audio/*.mp3, episodes.json, feed.xml
python tools/build.py          # 듣기 목록을 사이트에 다시 넣기
```

md를 고친 뒤 `build.py`만 다시 돌리면 사이트에 반영됩니다. PDF는 내용이 바뀌었을 때 `mkpdf.py`로 다시 만듭니다.

## 주의

실습에는 실제 개인정보·내부 문서를 넣지 않습니다. 모델 연표는 2026-10-15 기준이므로 강의 전에 최신 출시를 다시 확인합니다.
