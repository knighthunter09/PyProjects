import logging
import os
import sys
import time
import watchdog
import watchdog.events as ev
import watchdog.observers as ob

class FileHandlerCustom(ev.LoggingEventHandler):
    def on_any_event(self, event):
        print("I am a nerd")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = str(os.path.abspath(r"/Users/ISHI-VS/PycharmProjects/ProjectA"))
    event_handler = FileHandlerCustom()
    observer = ob.Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()