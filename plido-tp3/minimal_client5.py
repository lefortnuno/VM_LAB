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



temperature = virtual_sensor(start=20, variation = 0.1)
pressure    = virtual_sensor(start=1000, variation = 1)
humidity    = virtual_sensor(start=30, variation = 3, min=20, max=80)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    t = round(temperature.read_value()*100)
    p = round(pressure.read_value()*100)
    h = round(humidity.read_value()*100)

    j = [t, p, h]
    s.sendto (cbor.dumps(j), ("127.0.0.1", forward_port))
    print("Taille donnees: ", len(cbor.dumps(j)));
    time.sleep(2)
