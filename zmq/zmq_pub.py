import sys
import time
import zmq

context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind(sys.argv[1])

while True:
    time.sleep(1)
    sock.send_string(sys.argv[1] + ':' + time.ctime())