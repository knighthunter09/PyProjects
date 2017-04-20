import socket
import sys
import logging
import os
import sys
import time
import watchdog
import watchdog.events as ev
import watchdog.observers as ob

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address given on the command line
# server_name = sys.argv[1]
server_name = "localhost"
server_address = (server_name, 8085)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)
connection = None
client_address = None

class FileHandlerCustom(ev.LoggingEventHandler):
    def on_any_event(self, event):
        print("I am a nerd who generated these events " + str(event))
        if (connection):
            connection.sendall(bytearray(str(event), 'utf8'))

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
            #time.sleep(1)
            print(sys.stderr, 'waiting for a connection')
            connection, client_address = sock.accept()
            print(sys.stderr, 'client connected:', client_address)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        connection.close()
    observer.join()
