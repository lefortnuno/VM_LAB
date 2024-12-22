from virtual_sensor import virtual_sensor
import time
import socket
import json
import cbor2 as cbor
import kpn_senml as senml
import pprint
import binascii
import datetime
import time
import pprint

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


NB_ELEMENT = 5


temperature = virtual_sensor(start=20, variation = 0.1)
pressure    = virtual_sensor(start=1000, variation = 1)
humidity    = virtual_sensor(start=30, variation = 3, min=20, max=80)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def add_record(pack, name, unit, value):
    rec = senml.SenmlRecord(name, unit=unit, value=value)
    rec.time = time.mktime(datetime.datetime.now().timetuple())
    pack.add(rec)

while True:
    pack = senml.SenmlPack("device1")
    pack.base_time = time.mktime( datetime.datetime.now().timetuple())

    for k in range(NB_ELEMENT):
        t = round(temperature.read_value(), 2)
        h = round(humidity.read_value(), 2)
        p = int(pressure.read_value()*100) #Unit is Pa not hPa

        add_record(pack, "temperature", senml.SenmlUnits.SENML_UNIT_DEGREES_CELSIUS, t)
        add_record(pack, "humidity", senml.SenmlUnits.SENML_UNIT_RELATIVE_HUMIDITY, h)
        add_record(pack, "pressure", senml.SenmlUnits.SENML_UNIT_PASCAL, p)

        pprint.pprint(json.loads(pack.to_json()))
        pprint.pprint(cbor.loads(pack.to_cbor()))

        print ("JSON length: ", len(pack.to_json()), "bytes")
        print ("CBOR length: ", len(pack.to_cbor()), "bytes")

        time.sleep(10)

    s.sendto(pack.to_cbor(), ("127.0.0.1", forward_port))
