import sys
import subprocess
from parser import Parser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from server import app

md_files = []
def main():
    for i,arg in enumerate(sys.argv[1:]):
        p = Parser(arg)
        preview_path = p.method(i)
        md_files.append(".\\" + arg)
        command = ["powershell.exe", "-File","./preview.ps1" ] + [preview_path]
        #subprocess.run(command)
class MardownWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path in md_files:
            print(f"Text file modified: {event.src_path}")
            main()
if __name__ == "__main__":
    main()
    command = ["powershell.exe", "-File","./preview.ps1" ] + ["http://127.0.0.1:5000/0"]
    subprocess.run(command)
    path = "."
    event_handler = MardownWatcher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    # Start the observer
    observer.start()
    print(f"Monitoring directory: {path}")
    print(f"target files: {md_files}")
    app.run(debug=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()