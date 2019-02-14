import serial
import serial.tools.list_ports
import warnings
from threading import Thread
from time import sleep
import flask_server
import socket_server

sensor_state = [False, False, False, False, False]
sensor_count = [0]

def find_serial_device():
    ports = list(serial.tools.list_ports.comports())
    valid_ports = []
    for p in ports:
        if 'USB' in p.description or 'Arduino' in p.description:
            valid_ports.append(p)

    if not valid_ports:
        raise IOError("No USB serial devices found.")
    elif len(valid_ports) > 1:
        warnings.warn('Multiple USB serial devices found; using first.')

    return valid_ports[0]

def print_serial(device):
    sleep(1)
    while True:
        data = ser.readline().decode().strip()
        if data:
            print(data)

def read_serial(device):
    sleep(1)
    dummy_sensor_state = sensor_state.copy()
    while True:
        data = ser.readline().decode().strip()
        if data:
            for i in range(0, len(sensor_state)):
                sensor_state[i] = to_boolean(data[i])

        if dummy_sensor_state != sensor_state:
            dummy_sensor_state = sensor_state.copy()
            sensor_count[0] = total_active_sensors()
            #print(sensor_state)
        
def total_active_sensors():
    value = 0
    for sensor in sensor_state:
        if sensor:
            value += 1
    return value

def to_boolean(val):
    return (val != "0")

def run_socket_server():
    socket_server.SocketServer(sensor_state, sensor_count)

def run_flask_server():
    flask_server.FlaskServer()

t1 = Thread(target=run_socket_server, daemon=True)
t2 = Thread(target=run_flask_server, daemon=True)

t1.start()
t2.start()

try:
    device = find_serial_device()
    if device:
        print('Opening %s.' % device.description)
        ser = serial.Serial(device.device, 9600, timeout=.1)
        #print_serial(device)
        read_serial(device)
    else:
        print('Exiting')
except KeyboardInterrupt:
    if ser:
        ser.close()
        print('Closing %s' % device.description)
    print("Goodbye ʕ·͡ᴥ·ʔ")
    pass