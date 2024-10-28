import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from alert import send_alert
from database import log_file_access

logging.basicConfig(filename='file_tracker.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class FileTracker:
    def __init__(self, directory_to_watch):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def process(self, event):
        if event.event_type == 'created':
            logging.info(f"File created: {event.src_path}")
            log_file_access(event.src_path)
            send_alert(f"File created: {event.src_path}")
        elif event.event_type == 'modified':
            logging.info(f"File modified: {event.src_path}")
            log_file_access(event.src_path)
            send_alert(f"File modified: {event.src_path}")


    def on_modified(self, event):
        if not event.is_directory:
            self.process(event)

    def on_created(self, event):
        if not event.is_directory:
            self.process(event)
