import subprocess
import sys
import argparse
import os
import shutil
import serial
import struct
import time

def packIntegerAsULong(value):
    """Packs a python 4 byte unsigned integer to an arduino unsigned long"""
    return struct.pack('>I', value)    #should check bounds

parser = argparse.ArgumentParser(description='Programs and provisions bluz-based boards for test and production')
parser.add_argument('-s', '--port', default='', help='serial port for bluz')
opts = parser.parse_args()
print opts

port = opts.port

print "Welcome to bluz serial programmer!"

if port == '':
    print "You must specify a serial port to use"
    exit()

filename = raw_input("Enter the firmware filename: ")

filehandle = open(filename, 'rb')

print "Writing file contents to serial"
s = serial.Serial(port=port, baudrate=38400)

s.write('f')
s.flush()
print "Wrote size"
s.write(packIntegerAsULong(os.path.getsize(filename)))
s.flush()

sizeBack = s.readline()
print "Got size back: " + str(sizeBack)

i = 0
while i < os.path.getsize(filename):
    chunklength = 1024
    if os.path.getsize(filename) - i < 1024:
        chunklength = os.path.getsize(filename) - i
    filehandle.seek(i,0)
    chunk = filehandle.read(chunklength)
    s.write(chunk)
    s.readline()
    i+=1024

filehandle.close()
s.close()
