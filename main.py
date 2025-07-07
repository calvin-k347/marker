import sys
import subprocess
from parser import Parser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

md_files = []
def main():
    for arg in sys.argv[1:]:
        p = Parser(arg)
        preview_path = p.method()
        md_files.append(".\\" + arg)
        command = command = ["powershell.exe", "-File","./preview.ps1" ] + [preview_path]
        subprocess.run(command)
class MardownWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path in md_files:
            print(f"Text file modified: {event.src_path}")
            main()
if __name__ == "__main__":
    main()
    path = "."
    event_handler = MardownWatcher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    # Start the observer
    observer.start()
    print(f"Monitoring directory: {path}")
    print(f"target files: {md_files}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()