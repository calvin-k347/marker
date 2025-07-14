import sys
import subprocess
from parser import Parser
import time
from livereload import Server
from server import app, home
md_files = []
def main():
    for i,arg in enumerate(sys.argv[1:]):
        p = Parser(arg)
        preview_path = p.method(i)
        md_files.append(".\\" + arg)
if __name__ == "__main__":
    command = ["powershell.exe", "-File","./preview.ps1" ] + ["http://127.0.0.1/0"]
    server = Server(app.wsgi_app)
    server.watch("*.md", func=main)
    app.debug =True
    subprocess.run(command)
    server.serve(liveport=35729, host='127.0.0.1', port=80)
    