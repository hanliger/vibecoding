# 아주 작은 OTLP http/json 수신기: POST 본문을 그대로 한 줄씩 저장한다.
import sys, json
from http.server import BaseHTTPRequestHandler, HTTPServer
port, out = int(sys.argv[1]), sys.argv[2]
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        with open(out, 'ab') as f:
            f.write(json.dumps({"path": self.path, "ctype": self.headers.get('Content-Type')}).encode() + b"\n")
            f.write(body.replace(b"\n", b" ") + b"\n")
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers(); self.wfile.write(b"{}")
    def log_message(self, *a): pass
HTTPServer(('127.0.0.1', port), H).serve_forever()
