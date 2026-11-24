# OTLP(http/json) 수신 기록에서 구간(span) 이름, 부모 관계, 주요 속성을 뽑는다.
import json, sys, collections
spans, logs = [], []
lines = open(sys.argv[1]).read().splitlines()
for hdr, body in zip(lines[0::2], lines[1::2]):
    h = json.loads(hdr); d = json.loads(body)
    for rs in d.get("resourceSpans", []):
        res = {a["key"]: list(a["value"].values())[0] for a in rs["resource"].get("attributes", [])}
        for ss in rs.get("scopeSpans", []):
            for s in ss["spans"]:
                at = {a["key"]: list(a["value"].values())[0] for a in s.get("attributes", [])}
                spans.append((int(s["startTimeUnixNano"]), s["name"], s["spanId"], s.get("parentSpanId", ""), at, [e["name"] for e in s.get("events", [])], res))
    for rl in d.get("resourceLogs", []):
        for sl in rl.get("scopeLogs", []):
            for r in sl["logRecords"]:
                at = {a["key"]: list(a["value"].values())[0] for a in r.get("attributes", [])}
                logs.append(at.get("event.name", r.get("body", {}).get("stringValue", "?")))
spans.sort()
print("resource:", {k: v for k, v in spans[0][6].items() if k.startswith(("service", "host", "os"))} if spans else None)
print("span counts:", collections.Counter(s[1] for s in spans))
print("log events:", collections.Counter(logs))
ids = {s[2]: s[1] for s in spans}
keep = ["tool_name", "file_path", "full_command", "bash_argv0", "success", "decision", "model", "input_tokens", "output_tokens", "cache_read_tokens", "duration_ms", "error", "user_prompt_length", "stop_reason"]
for t, name, sid, pid, at, ev, _ in spans:
    sel = {k: (str(at[k])[:70]) for k in keep if k in at}
    print(f"{name:34s} parent={ids.get(pid, '-'):24s} {sel} events={ev}")
