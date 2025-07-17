import sys
import subprocess
from parser import Parser
import time
from livereload import Server
from server import app, home
def parse(file,i):
    Parser(file).method(i)
if __name__ == "__main__":
    for i, arg in enumerate(sys.argv[1:]):
        Parser(arg).method(i)
    if sys.platform ==  "win32":
        start_tailwind = ["powershell.exe", "-File", "./scripts/build_tailwind.ps1"]
        start_preview = ["powershell.exe", "-File","./scripts/preview.ps1" ] + ["http://127.0.0.1/0"]
    server = Server(app.wsgi_app)
    for i, file in enumerate(sys.argv[1:]):
        server.watch(file, func=lambda: parse(file,i))
    app.debug =True
    subprocess.run(start_tailwind)
    subprocess.run(start_preview)
    server.serve(liveport=35729, host='127.0.0.1', port=80)
    