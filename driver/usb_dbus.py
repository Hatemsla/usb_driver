# usb_dbus.py
from dasbus.server.interface import dbus_interface
from dasbus.typing import Str, List, UInt16
import constansts as cons
import usb_driver

@dbus_interface(cons.DOMEN)
class UsbDriver():

    def Connect(self) -> Str:
        try:
            usb_driver.dev = usb_driver.find_device()
            usb_driver.init(usb_driver.dev)

            print("Successfully connected to USB")
            
            return "Successfully connected to USB"
        except Exception as e:
            print("Error connecting to USB")
            return "Error connecting to USB"

    def GetStatus(self) -> Str:
        try:
            usb_driver.ret = usb_driver.control_read(usb_driver.dev, cons.VENDOR_VERSION, 0, 0, 0x02)
            
            print("Connected to USB")
            
            return "Connected to USB"
        except Exception as e:
            print("Device not found")
            return "Device not found"

    def GetData(self) -> List[int]:
        try:
            ret = usb_driver.dev.read(cons.READ_PORT, cons.PACKAGE_SIZE, cons.USB_TIMEOUT_MILLIS)
            # print(str(ret, 'cp1251'))
            ret_list = list(ret)
            print(ret_list)
            return ret_list
            # print(str(ret))
            # return str(ret)
        except Exception as e:
            print(e)
            return "Error reading from USB"
    
