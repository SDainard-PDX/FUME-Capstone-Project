import serial
from serial.tools import list_ports as lsports
from serial.tools.list_ports_common import ListPortInfo

import time

devices = []
connected_dev = None
serial_conn : serial.Serial = None 

def connect_to_port():
    global connected_dev, serial_conn
    if not isinstance(connected_dev, ListPortInfo):
        return False
    
    serial_conn = serial.Serial(connected_dev.device, baudrate=9600)
    time.sleep(2)
    serial_conn.reset_output_buffer()
    serial_conn.reset_input_buffer()

devices = lsports.comports(True)
i = 0
for dev in devices:
    print(f"{i}:", dev.description)
    i += 1

sel = int(input())
connected_dev = devices[sel]

if not connected_dev is None:
    connect_to_port()
    while True:
        msg = input("send to microcontroller: ").encode('ascii')
        serial_conn.write(msg)
        print(serial_conn.read(len(msg)))



