import sys
import zmq

context = zmq.Context()
sock = context.socket(zmq.PULL)

for arg in sys.argv[1:]:
    sock.connect(arg)

while True:
    message= sock.recv()
    print(message)