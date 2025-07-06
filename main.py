import sys
import subprocess
from parser import Parser
for arg in sys.argv[1:]:
    p = Parser(arg)
    preview_path = p.method()
    command = command = ["powershell.exe", "-File","./preview.ps1" ] + [preview_path]
    subprocess.run(command)
