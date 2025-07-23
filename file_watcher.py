#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime

class PythonFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self._handle_event(event, "🔄 File modified")

    def on_created(self, event):
        self._handle_event(event, "✨ New Python file created")

    def _handle_event(self, event, message):
        if event.is_directory or not event.src_path.endswith('.py'):
            return
        filename = os.path.basename(event.src_path)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}: {filename}")
        self._take_action(event.src_path)

    def _take_action(self, file_path):
        try:
            subprocess.run(['manim', file_path, '-pql'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while rendering the file with manim: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
        print("-" * 60)

def start_watcher(path="."):
    abs_path = os.path.abspath(path)
    event_handler = PythonFileHandler()
    observer = Observer()
    observer.schedule(event_handler, abs_path, recursive=True)
    observer.start()
    print(f"👀 Watching for Python file changes in: {abs_path}")
    print("Press Ctrl+C to stop watching")
    print("-" * 60)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nFile watching stopped")
    observer.join()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    start_watcher(path)