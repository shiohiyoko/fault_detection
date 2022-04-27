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
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd


class SpreadSheet():
    def __init__(self, oauth_json, spreadsheet_name):
        self.GDOCS_OAUTH_JSON       = oauth_json

        # Google Docs spreadsheet name.
        self.GDOCS_SPREADSHEET_NAME = spreadsheet_name

        self.workbook = self.login_open_sheet(self.GDOCS_OAUTH_JSON, self.GDOCS_SPREADSHEET_NAME)
    
    def login_open_sheet(self, oauth_key_file, spreadsheet):
        """Connect to Google Docs spreadsheet and return the first worksheet."""
        try:
            scope =  ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
            gc = gspread.authorize(credentials)
            worksheet = gc.open(spreadsheet)
            return worksheet

        except Exception as ex:
            print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
            print('Google sheet login failed with error:', ex)
            sys.exit(1)

    # append data to state sheet
    def append(self, data, title = "Sheet1"):
        try:
            # create worksheet if doesn't exist
            if self.find(title) is False:
                self.workbook.add_worksheet(title=title, rows=100, cols=4)
            
            # open worksheet and append data
            worksheet = self.workbook.worksheet(title)
            # worksheet.append_row(data)
            gd.set_with_dataframe(worksheet, data)

        except Exception as e:
            print('Append error, log in again')
            error(e)
            self.workbook = None
            time.sleep(10)

    # find title from worksheets
    def find(self, title):
        for tmp in self.workbook.worksheets():
            if tmp.title == title:
                return True
        
        return False
        

class GetData(object):
    def __init__(self):
        self.port = '/dev/ttyUSB0'
        self.baudrate = 115200
        print("Open Port")
        self.device = XBeeDevice(self.port, self.baudrate)
        self.raw_data = {'time':[], 
                         'id':[], 
                         'temperature':[],
                         'vibration':[],
                         'current':[]}

        try:
            self.device.open()
        
            self.device.add_data_received_callback(self.get_data)
            print("Waiting for data....")

        except Exception as e:
            error(e)

    def get_data(self, xbee_message):
        temp = xbee_message.data
        # print(xbee_message.remote_device.get_64bit_addr())
        print("data received!")
        self.raw_data['time'].append(int(time.time()))
        self.raw_data['id'].append(xbee_message.remote_device.get_64bit_addr())
        self.raw_data['temperature'].append(int.from_bytes(temp[0:2], byteorder='big', signed=True) * 0.01)
        self.raw_data['vibration'].append(int.from_bytes(temp[2:4], byteorder='big', signed=True))   
        self.raw_data['current'].append(int.from_bytes(temp[4:6], byteorder='big', signed=True))
        
        # df = pd.DataFrame(data=value, columns=['id', 'vibration', 'temperature'])
        # return value
        # print(self.raw_data[:][-1])

        # value = self.ser.readline()
        # value = value.decode()
        # value = value.rstrip() 
        # return value.split(',')       

    def saveData(self):
        print("saving data ...")
        df = pd.DataFrame(self.raw_data)
        fname = 'test.csv'
        df.to_csv(fname)
        # with open('test.csv', 'w') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(df.values)
        
    def ser_close(self):
        print("Close Port")
        if self.device is not None and self.device.is_open():
            self.device.close()
    
    def clearData(self):
        for data in self.raw_data.values():
            data.clear()


GDOCS_OAUTH_JSON       = '/home/shiohiyoko/MemoRi/fault_detection/dht22_spread/propane-net-346716-96d30a3aef97.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'database'

data = GetData()
sp = SpreadSheet(GDOCS_OAUTH_JSON,GDOCS_SPREADSHEET_NAME)

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
while True:

    df = pd.DataFrame(data.raw_data)
    sp.append(df)
    data.clearData()
    time.sleep(1)

# input()
# data.saveData()
# data.ser_close()