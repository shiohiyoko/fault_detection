import serial
from serial.serialutil import *

from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import pandas as pd
import numpy
import csv
import pprint
import time

class GetData(object):

    def __init__(self):
        self.port = '/dev/ttyACM0'
        self.baudrate = 115200
        print("Open Port")
        self.ser = serial.Serial(self.port, self.baudrate, timeout=None)

    def get_data(self):
        value = self.ser.readline()
        value = value.decode()
        value = value.rstrip() 
        return value.split(',')        

        # df = pd.DataFrame(data=value, columns=['id', 'vibration', 'temperature'])
        # return value

    def ser_close(self):
        print("Close Port")
        self.ser.close()

data = GetData()
x = []
y = []
CNT = 20
data_size = 3

fig, ax = plt.subplots()
lines, = ax.plot(x, y)

ax.set_xlim((0, CNT))
ax.set_ylim((-10, 20))

for i in range(CNT):
    raw_data = data.get_data()
    # print(raw_data)
    if len(raw_data) == data_size:
        print(raw_data)
        raw_data.append(int(time.time()))
        # x.append(i)
        # y.append(float(raw_data[0]))
        # lines.set_data(x, y)
        # plt.pause(0.01)

        with open(raw_data[0]+'.csv', 'a') as f:
            writer = csv.writer(f)
            
            writer.writerow(raw_data)

data.ser_close()