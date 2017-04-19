import logging
import os
import sys
import time
import watchdog
import watchdog.events as ev
import watchdog.observers as ob
import zmq
import socket


def createSocket(sock_pull):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_name = "localhost"
    server_address = (server_name, 8084)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)
    sock.listen(1)
    return sock
'''
    while True:
        print(sys.stderr, 'waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print(sys.stderr, 'client connected:', client_address)
            while True:
                message = sock_pull.recv()
                print("Message received " + message)
                connection.sendall(bytearray("hello22", 'utf8'))
        finally:
            connection.close()
'''

if __name__ == "__main__":

    context = zmq.Context()
    sock_push = context.socket(zmq.PUSH)
    # sock_push.bind(sys.argv[1])
    sock_push.bind(r"tcp://*:8083")

    sock_pull = context.socket(zmq.PULL)
    # sock_pull.bind(sys.argv[1])
    sock_pull.connect(r"tcp://localhost:8083")

    sock = createSocket(sock_pull)

    class FileHandlerCustom(ev.LoggingEventHandler):
        def on_any_event(self, event):
            print("I am a nerd -- " + str(event.event_type))
            print(sock_push)
            sock_push.send_string(str(event.event_type))


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
            try:
                while True:
                    message = sock_pull.recv()
                    print("Message received " + message)
                    connection.sendall(bytearray("hello22", 'utf8'))
            finally:
                connection.close()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()





