from digi.xbee.devices import XBeeDevice

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 115200


def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        def data_receive_callback(xbee_message):
            # print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
            #                          xbee_message.data))
            temp = xbee_message.data
            # print(temp)

            print("temp: ",int.from_bytes(temp[0:2], byteorder='big', signed=True) * 0.01)
            print("vib:  ",int.from_bytes(temp[2:4], byteorder='big', signed=True))
            print("curr: ",int.from_bytes(temp[4:6], byteorder='big', signed=True))
        
        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()
    except Exception as e:
        print(e)
    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()