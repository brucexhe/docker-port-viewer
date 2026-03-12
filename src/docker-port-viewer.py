#!/usr/bin/python3
import http.server
import socketserver
import subprocess

PORT = 16888

class DockerPortHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 响应 HTTP 头
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # 准备 HTML 网页骨架（内置简单的 CSS 美化）
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Docker Port Viewer</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; background-color: #f5f6fa; }
                h1 { color: #2f3640; }
                table { border-collapse: collapse; width: 100%; max-width: 1000px; background-color: white; box-shadow: 0 1px 3px rgba(0,0,0,0.2); border-radius: 8px; overflow: hidden; }
                th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #dcdde1; line-height: 1.5; }
                th { background-color: #00a8ff; color: white; font-weight: bold; }
                tr:hover { background-color: #f1f2f6; }
                .error { color: #e84118; font-weight: bold; }
                .empty { color: #7f8fa6; font-style: italic; }
            </style>
        </head>
        <body>
            <h1>🐳 Docker Port Viewer</h1>
            <table>
                <tr><th>Docker 容器名称</th><th>映射的端口号</th></tr>
        """

        try:
            # 执行群晖底层的 docker ps 命令
            cmd =['/usr/local/bin/spm-exec', 'docker', 'ps', '--format', '{{.Names}}|{{.Ports}}']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                html += f"<tr><td colspan='2' class='error'>无法连接到 Docker 服务。请确保 Docker 已运行且本套件拥有权限。<br>{result.stderr}</td></tr>"
            else:
                lines = result.stdout.strip().split('\n')
                if not lines or lines == ['']:
                    html += "<tr><td colspan='2' class='empty'>当前没有正在运行的 Docker 容器。</td></tr>"
                else:
                    # 解析并渲染每一行数据
                    for line in lines:
                        if not line: continue
                        parts = line.split('|', 1)
                        name = parts[0]
                        ports = parts[1] if len(parts) > 1 and parts[1] else "无映射端口"
                        html += f"<tr><td><b>{name}</b></td><td>{ports}</td></tr>"
        except Exception as e:
            html += f"<tr><td colspan='2' class='error'>发生内部异常: {str(e)}</td></tr>"

        html += """
            </table>
        </body>
        </html>
        """
        # 返回网页给浏览器
        self.wfile.write(html.encode('utf-8'))

print(f"Starting Docker Port Viewer on port {PORT}...")
with socketserver.TCPServer(("", PORT), DockerPortHandler) as httpd:
    httpd.serve_forever()