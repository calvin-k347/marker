from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class MardownWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".md"):
            print(f"Text file modified: {event.src_path}")

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('new.html')
if __name__ == "__main__":
    path = "."  # Directory to monitor (current directory in this case)
    event_handler = MardownWatcher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    # Start the observer
    observer.start()
    print(f"Monitoring directory: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()