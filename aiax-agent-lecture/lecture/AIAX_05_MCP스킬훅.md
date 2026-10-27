---
title: 5강 · MCP·스킬·훅으로 자동화하기
part: 본강
order: 5
time: 25분
desc: MCP로 자료를 연결하고, 스킬로 반복 업무를 묶고, 훅으로 실수를 막는 법을 직접 만들어 봅니다.
practice: 70%
nav: 5강. MCP·스킬·훅
tags: [MCP, 스킬, 훅, ClaudeCode, 자동화]
---

# 5강. MCP·스킬·훅으로 자동화하기

![[images/aiax_ig_05_tools.png|MCP는 손발, 스킬은 업무 수첩, 훅은 꼭 지키는 약속]]

> [!question] 생각해 보기
> 신규 직원이 업무 수첩(4강)을 받았습니다. 그래도 공유폴더에 접근을 못 하고, 매주 하는 보고서 양식을 모르고, 원본 서류를 실수로 버릴 수 있습니다. 무엇을 더 줘야 할까요?

## 0. 한 줄 흐름

```mermaid
graph LR
    A["밖의 자료에 손이 안 닿는다"] --> B["MCP<br/>손과 발"]
    B --> C["반복 업무를 매번 설명한다"] --> D["스킬<br/>업무 매뉴얼"]
    D --> E["지켜야 할 규칙을 잊는다"] --> F["훅<br/>강제 규칙"]
```

| 장치 | 비유 | 역할 | 누가 실행하나 |
|---|---|---|---|
| MCP | 손과 발 | 외부 도구·데이터 연결 | 에이전트가 필요할 때 호출 |
| 스킬 | 업무 매뉴얼 | 반복 업무 절차 묶음 | 에이전트가 상황을 보고 꺼내 씀 |
| 훅 | 자동 규칙 | 특정 시점에 무조건 실행 | 시스템이 강제 실행 |

## 1. 문제: 밖의 자료에 손이 안 닿는다 → MCP

> [!abstract] 약어 풀이
> MCP: Model Context Protocol. 에이전트가 파일, 드라이브, 메신저, DB 같은 외부 도구에 같은 방식으로 연결되는 표준 규격. USB 단자처럼 꽂으면 연결됩니다.

> [!example] 바로 해 보기: 파일 MCP 연결
> 1. 터미널에서 아래를 입력합니다.
> ```bash
> claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem ./data
> claude mcp list
> ```
> 2. Claude Code 세션에서 `/mcp`를 입력해 연결 상태를 봅니다.
> 3. "data 폴더 파일 목록 보여줘"라고 지시합니다.
> 성공 확인: 연결 상태가 connected이고 파일 목록이 나오면 성공.

팀이 함께 쓰려면 프로젝트에 `.mcp.json`으로 남깁니다.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    }
  }
}
```

구글 드라이브, 슬랙, 노션, DB도 같은 방식으로 연결합니다.

## 2. 문제: 반복 업무를 매번 설명한다 → 스킬

`.claude/skills/weekly-report/SKILL.md`

```markdown
---
name: weekly-report
description: 주간 업무보고서 작성 요청 시 사용. data/ 엑셀을 읽어 output/에 보고서 md를 만든다.
---

# 주간 업무보고 작성 절차
1. data/ 폴더의 최신 엑셀을 읽는다
2. 항목별 건수와 전주 대비 증감을 계산한다
3. output/주간보고_YYYYMMDD.md로 저장한다
   - 제목 / 주요 실적(3줄) / 수치 표 / 다음 주 계획
4. 표 합계가 원본과 일치하는지 검증하고 결과를 보고한다
```

> [!tip] 핵심
> `description`이 "언제 이 스킬을 꺼낼지"를 정합니다. 어떤 요청에 쓰는지 구체적으로 씁니다.

> [!example] 바로 해 보기: 스킬 호출
> 1. 위 파일을 그대로 만듭니다.
> 2. 새 세션에서 "이번 주 주간보고 만들어줘"라고만 지시합니다.
> 성공 확인: 에이전트가 weekly-report 스킬을 불러와 양식대로 output/에 저장하면 성공.

## 3. 문제: 지켜야 할 규칙을 잊는다 → 훅

훅(Hook)은 정해진 시점에 무조건 실행됩니다. 에이전트가 "깜빡"할 수 없습니다.

| 이벤트 | 시점 | 쓰임 |
|---|---|---|
| PreToolUse | 도구 실행 전 | 위험 명령 차단 (종료 코드 2) |
| PostToolUse | 도구 실행 후 | 변경 기록, 서식 정리 |
| UserPromptSubmit | 지시 입력 시 | 규칙 자동 주입 |
| Stop | 작업 종료 시 | 테스트 실행, 알림 |

**예시: 원본 폴더 삭제·이동 차단 + 변경 기록**

`.claude/hooks/protect-data.sh`

```bash
#!/bin/bash
# 표준입력으로 받은 도구 정보에서 명령어를 꺼낸다
cmd=$(jq -r '.tool_input.command // ""')
if echo "$cmd" | grep -q 'data/' && echo "$cmd" | grep -qE '(^|[[:space:]])(rm|mv)[[:space:]]'; then
  echo "data/ 원본은 삭제·이동할 수 없습니다" >&2
  exit 2
fi
exit 0
```

`.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "bash .claude/hooks/protect-data.sh" } ] }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write",
        "hooks": [ { "type": "command",
          "command": "jq -r '.tool_input.file_path' >> output/change.log" } ] }
    ]
  }
}
```

> [!example] 바로 해 보기: 훅이 막는지 확인
> 1. `chmod +x .claude/hooks/protect-data.sh` 후 세션을 다시 시작합니다.
> 2. "data 폴더의 엑셀을 지워줘"라고 지시합니다.
> 3. 아무 파일이나 수정을 지시한 뒤 `output/change.log`를 엽니다.
> 성공 확인: 삭제가 막히고, change.log에 수정한 파일 경로가 남으면 성공.

> [!warning] 강사 메모
> 훅은 강제 실행되므로 잘못 쓰면 모든 작업이 막힙니다. 강의 전 실습 환경에서 위 두 훅을 직접 돌려 보고 시연합니다. `jq` 설치가 필요합니다.

## 정리

### 1분 요약

MCP는 손발(외부 연결), 스킬은 업무 매뉴얼(반복 절차), 훅은 강제 규칙(무조건 실행). 매번 설명하던 것을 파일로 남기면 에이전트가 같은 품질로 반복합니다.

### 문제 → 해결책 짝 맞추기

| 문제 | 해결책 |
|---|---|
| 외부 자료·도구에 닿지 않는다 | MCP |
| 반복 업무를 매번 설명한다 | 스킬 (SKILL.md) |
| 규칙을 잊거나 어긴다 | 훅 (PreToolUse 차단, PostToolUse 기록) |
| 스킬이 안 불린다 | description을 구체적으로 |

### 이 단계에서 쓰는 도구

- `claude mcp add`, `/mcp`, `.mcp.json`
- `.claude/skills/<이름>/SKILL.md`
- `.claude/settings.json`의 hooks, jq

### 셀프 체크

- [ ] MCP·스킬·훅을 비유로 구분해 말할 수 있다
- [ ] MCP 서버 1개를 연결했다
- [ ] 내 업무용 SKILL.md 초안 1개를 썼다
- [ ] 훅이 실제로 차단하는 것을 확인했다

### AI에게 더 잘 요청하기

| 막연한 요청 | 용어를 넣은 요청 |
|---|---|
| 이거 자동으로 해줘 | 이 절차를 SKILL.md로 만들어줘. description은 "출동통계 월보 요청 시 사용" |
| 실수 안 하게 해줘 | data/ 삭제를 막는 PreToolUse 훅을 만들고, 테스트 방법도 알려줘 |

### 더 찾아볼 곳

- [Model Context Protocol 공식 사이트](https://modelcontextprotocol.io)
- [Claude Code 훅 문서](https://docs.claude.com/en/docs/claude-code/hooks)
- [Claude Code 스킬 문서](https://docs.claude.com/en/docs/claude-code/skills)

```quiz
{"title":"5강 확인 퀴즈","questions":[
{"q":"에이전트를 외부 도구·데이터에 연결하는 표준 규격은?","options":["MCP","SKILL.md","CLAUDE.md","PreToolUse"],"answer":0,"explain":"MCP는 Model Context Protocol입니다."},
{"q":"스킬이 언제 쓰일지를 결정하는 항목은?","options":["name","description","파일 크기","폴더 색"],"answer":1,"explain":"description을 보고 에이전트가 스킬을 꺼냅니다."},
{"q":"에이전트의 판단과 상관없이 정해진 시점에 무조건 실행되는 것은?","options":["스킬","MCP","훅","서브에이전트"],"answer":2,"explain":"훅은 시스템이 강제로 실행합니다."},
{"q":"위험한 명령을 실행 전에 막으려면 어떤 이벤트를 쓰나?","options":["PostToolUse","PreToolUse","Stop","UserPromptSubmit"],"answer":1,"explain":"PreToolUse에서 종료 코드 2를 돌려주면 차단됩니다."},
{"q":"MCP·스킬·훅의 비유로 바른 짝은?","options":["손발·매뉴얼·강제 규칙","매뉴얼·손발·강제 규칙","강제 규칙·손발·매뉴얼","손발·강제 규칙·매뉴얼"],"answer":0,"explain":"MCP는 손발, 스킬은 매뉴얼, 훅은 강제 규칙입니다."}
]}
```
