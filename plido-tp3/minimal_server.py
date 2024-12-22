
import socket
import binascii

import socket
import binascii
import argparse
import cbor2 as cbor


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


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((forward_address, forward_port))

t = []
p = []
h = []
size_max=0

while True:
    data, addr = s.recvfrom(1024)
    donnees = cbor.loads(data)

    if len(data) > size_max :
       size_max = len(data)

    t.append(donnees[0] / 100)
    p.append(donnees[1] / 100)
    h.append(donnees[2] / 100)

    mt = sum(t)/len(t)
    mp = sum(p)/len(p)
    mh = sum(h)/len(h)

    print("Taille donnees maximale recus: ",size_max," octets")
    print ("Donnees(t,p,h)=>",donnees)
    print ("Moyenne(t,p,h)=>", mt, mp, mh,"\n")
