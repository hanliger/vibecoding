#!/bin/bash
# 사용법: run_agent.sh <run 디렉터리> <OTLP 포트>
R=$1; P=$2; S=$(dirname "$R")
python3 -I "$(dirname "$0")/otlp_recv.py" $P "$R/otlp.jsonl" & RECV=$!
cd "$R/click"
{ date -Iseconds; claude --version; uname -sr; ../venv/bin/python --version; git rev-parse --short HEAD; } > "$R/env.txt" 2>&1
PATH="$R/venv/bin:$PATH" \
CLAUDE_CODE_ENABLE_TELEMETRY=1 CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1 \
OTEL_TRACES_EXPORTER=otlp OTEL_METRICS_EXPORTER=none OTEL_LOGS_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_PROTOCOL=http/json OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:$P \
OTEL_TRACES_EXPORT_INTERVAL=1000 OTEL_LOGS_EXPORT_INTERVAL=1000 \
OTEL_LOG_USER_PROMPTS=1 OTEL_LOG_TOOL_DETAILS=1 OTEL_LOG_TOOL_CONTENT=1 \
timeout 1200 claude -p "$(cat "$S/prompt.txt")" \
  --model claude-sonnet-5-5 --max-turns 40 \
  --setting-sources project --strict-mcp-config \
  --output-format stream-json --verbose \
  --allowedTools "Read" "Edit" "Write" "Glob" "Grep" "Bash(python:*)" "Bash(pytest:*)" "Bash(git diff:*)" "Bash(git status:*)" "Bash(git log:*)" "Bash(git show:*)" \
  --disallowedTools "WebFetch" "WebSearch" \
  > "$R/stream.jsonl" 2> "$R/stderr.txt"
echo "exit=$?" >> "$R/env.txt"
date -Iseconds >> "$R/env.txt"
sleep 10; kill $RECV
git -C "$R/click" diff > "$R/agent.diff"; git -C "$R/click" status --short > "$R/status.txt"
