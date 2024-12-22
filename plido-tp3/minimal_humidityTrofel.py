from virtual_sensor import virtual_sensor
import time
import socket
import cbor2 as cbor

import socket
import binascii
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="show uplink and downlink messages")
parser.add_argument('--http_port',  default=9999,
                    help="set http port for POST requests")
parser.add_argument('--forward_address',  default='127.0.0.1',
                    help="IP address to forward packets")

args = parser.parse_args()
verbose = args.verbose
defPort = int(args.http_port)
if defPort == 9999:
    forward_port = 33033
else: #if a port is specified, the loopback port is also change
    forward_port = defPort+5683
forward_address = args.forward_address



humidity = virtual_sensor(start=30, variation = 3, min=20, max=80)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

intervalSend = 10 #5min
intervalCollect = 2 #10s
isTime = 0 
h_data = []
i = 0

while True:

    h = round(humidity.read_value()*100)

    if i == 0:
       h_data.append(h)
    elif i == 1:
       h_data.append(h - h_data[0])
    else:
       delta = h - h_data[0] - h_data[i-1]
       h_data.append(delta)

    i += 1
    print (len(h_data), len(cbor.dumps(h_data)), h_data)

    # Sending data after 5min.
    if isTime >= intervalSend:
        print ("send => ",h_data)
        s.sendto (cbor.dumps(h_data), ("127.0.0.1", forward_port))
        h_data = []
        isTime = 0
        i = 0

    isTime += intervalCollect
    time.sleep(intervalCollect)
