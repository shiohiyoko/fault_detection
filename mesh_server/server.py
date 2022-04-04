from distutils.log import error
from digi.xbee.devices import XBeeDevice

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
        self.port = '/dev/ttyUSB0'
        self.baudrate = 115200
        print("Open Port")
        self.device = XBeeDevice(self.port, self.baudrate)
        self.raw_data = [[],[],[],[]]

        try:
            self.device.open()
        
            self.device.add_data_received_callback(self.get_data)
            print("Waiting for data....")

        except Exception as e:
            error(e)

    def get_data(self, xbee_message):
        temp = xbee_message.data
        self.raw_data[0].append(int(time.time()))
        self.raw_data[1].append(int.from_bytes(temp[0:2], byteorder='big', signed=True) * 0.01)
        self.raw_data[2].append(int.from_bytes(temp[2:4], byteorder='big', signed=True))   
        self.raw_data[3].append(int.from_bytes(temp[4:6], byteorder='big', signed=True))
        # df = pd.DataFrame(data=value, columns=['id', 'vibration', 'temperature'])
        # return value


        # value = self.ser.readline()
        # value = value.decode()
        # value = value.rstrip() 
        # return value.split(',')       

    def saveData(self):
        print("saving data ...")
        df = pd.DataFrame(self.raw_data).T
        with open('test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(df.values)
        
    def ser_close(self):
        print("Close Port")
        if self.device is not None and self.device.is_open():
            self.device.close()

data = GetData()
# x = []
# y = []
# CNT = 20
# data_size = 3

# fig, ax = plt.subplots()
# lines, = ax.plot(x, y)

# ax.set_xlim((0, CNT))
# ax.set_ylim((-10, 20))

# for i in range(CNT):
#     raw_data = data.get_data()
#     # print(raw_data)
#     if len(raw_data) == data_size:
#         print(raw_data)
#         raw_data.append(int(time.time()))
#         # x.append(i)
#         # y.append(float(raw_data[0]))
#         # lines.set_data(x, y)
#         # plt.pause(0.01)

#         with open(raw_data[0]+'.csv', 'a') as f:
#             writer = csv.writer(f)
            
#             writer.writerow(raw_data)

# data.ser_close()

input()
data.saveData()
data.ser_close()