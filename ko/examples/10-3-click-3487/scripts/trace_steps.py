# stream-json 기록에서 에이전트의 행동 순서를 한 줄씩 뽑는다.
import json, sys
for line in open(sys.argv[1]):
    m = json.loads(line)
    t = m.get("type")
    if t == "system" and m.get("subtype") == "init":
        print("INIT model=", m.get("model"), "tools=", len(m.get("tools", [])), "cwd=", m.get("cwd")[-20:])
    elif t == "assistant":
        for c in m["message"]["content"]:
            if c["type"] == "text" and c["text"].strip():
                print("  SAY :", c["text"].strip().replace("\n", " ")[:160])
            elif c["type"] == "tool_use":
                i = c["input"]
                arg = i.get("command") or i.get("file_path") or i.get("pattern") or ""
                extra = ""
                if c["name"] == "Read" and i.get("offset"): extra = f" (offset {i['offset']}, limit {i.get('limit')})"
                print("  TOOL:", c["name"], str(arg).replace("\n", " ")[:150], extra)
    elif t == "user":
        for c in m["message"]["content"]:
            if isinstance(c, dict) and c.get("type") == "tool_result":
                cont = c.get("content")
                if isinstance(cont, list): cont = " ".join(x.get("text", "") for x in cont if isinstance(x, dict))
                s = str(cont).strip().splitlines()
                print("    -> ", ("ERR " if c.get("is_error") else "") + (s[-1][:130] if s else ""))
    elif t == "result":
        print("RESULT turns=", m.get("num_turns"), "dur_ms=", m.get("duration_ms"), "cost_usd=", m.get("total_cost_usd"), "usage=", {k: v for k, v in m.get("usage", {}).items() if "tokens" in k})
