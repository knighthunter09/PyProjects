import logging
import os
import sys
import time
import watchdog
import watchdog.events as ev
import watchdog.observers as ob
import zmq

if __name__ == "__main__":

    context = zmq.Context()
    sock_push = context.socket(zmq.PUSH)
    # sock_push.bind(sys.argv[1])
    sock_push.bind(r"tcp://*:8083")

    class FileHandlerCustom(ev.LoggingEventHandler):
        def on_any_event(self, event):
            print("I am a nerd wow-- " + str(event.event_type))
            print(sock_push)
            sock_push.send_string(str(event.event_type))

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = str(os.path.abspath(r"C:\Users\e816824\Downloads\Python_Pandas_Ex1-master\Python_Pandas_Ex1-master"))
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




