import sys
import zmq
import socket


def createSocket(sock_pull):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_name = "localhost"
    server_address = (server_name, 8084)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)
    return sock

if __name__ == "__main__":

    context = zmq.Context()
    sock_pull = context.socket(zmq.PULL)
    sock_pull.connect(r"tcp://localhost:8083")

    sock = createSocket(sock_pull)
    sock.listen(1)

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





