# usb_dbus.py
from dasbus.server.interface import dbus_interface
from dasbus.typing import Str, List
import constansts as cons
import usb_driver
import traceback 

@dbus_interface(cons.DOMEN)
class UsbDriver():

    def __init__(self):
        self.data = []
        self.result_data = []
        self.remain_data = []

    def Connect(self) -> Str:
        try:
            usb_driver.dev = usb_driver.find_device()
            usb_driver.init(usb_driver.dev)

            print("Successfully connected to USB")
            
            return "Successfully connected to USB"
        except Exception as e:
            print("Error connecting to USB " + str(e))
            return "Error connecting to USB"

    def GetStatus(self) -> Str:
        try:
            # usb_driver.ret = usb_driver.control_read(usb_driver.dev, cons.VENDOR_VERSION, 0, 0, 0x02)
            usb_driver.ret = usb_driver.ep_read.read(cons.PACKAGE_SIZE, cons.USB_TIMEOUT_MILLIS)
            
            print("Connected to USB")
            
            return "Connected to USB"
        except Exception as e:
            print("Device not found")
            return "Device not found"

    def GetData(self) -> List[int]:
        try:
            # print(usb_driver.ep_read)
            
            while True:
                ret = list(usb_driver.ep_read.read(cons.PACKAGE_SIZE))
                
                print(ret)
                
                if ret[0] != 253 and self.remain_data == []:
                    continue
                
                self.data += ret
                
                if self.remain_data != []:
                    self.data = self.remain_data + self.data
                    self.remain_data = []
                
                print("No valid packet: ", self.data)
                
                self.result_data = []
                
                while True:
                    if len(self.data) >= 2:
                        payload_length = self.data[1]
                        
                        if len(self.data) == payload_length + 12:
                            self.result_data += self.data
                            self.data = []
                            print("Result data: ", self.result_data)
                            return self.result_data
                        elif len(self.data) > payload_length + 12:
                            self.result_data += self.data[:payload_length + 12]
                            print("Data: ", self.data)
                            self.data = self.data[payload_length + 12:]
                        else:
                            self.remain_data += self.data
                            self.data = []
                            print("Remain data: ", self.remain_data)
                            print("Result data: ", self.result_data)
                            return self.result_data
                    else:
                        self.remain_data += self.data
                        self.data = []
                        print("Remain data: ", self.remain_data)
                        print("Result data: ", self.result_data)
                        return self.result_data
        except Exception as e:
            print(e)
            traceback.print_exc()
            return []
        
    
    def SendData(self, msg: List[int]) -> Str:
        try:
            # ret = usb_driver.ep_write.write(msg, cons.USB_TIMEOUT_MILLIS)
            # print(ret)
            return 'Successfully sent data'
        except Exception as e:
            print(e)
            return "Error writing to USB"
        