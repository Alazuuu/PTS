import serial
import time
import string
import pynmea2


def gps():
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline()
    if newdata[0:6] in "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        cordinate = (lat, lng)
        cordinate = (10, 20)
        return cordinate
