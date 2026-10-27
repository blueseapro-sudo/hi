#!/bin/bash
# 표준입력으로 받은 도구 정보에서 명령어를 꺼낸다
cmd=$(jq -r '.tool_input.command // ""')
if echo "$cmd" | grep -q 'data/' && echo "$cmd" | grep -qE '(^|[[:space:]])(rm|mv)[[:space:]]'; then
  echo "data/ 원본은 삭제·이동할 수 없습니다" >&2
  exit 2
fi
exit 0
