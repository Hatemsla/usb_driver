# main.py
import threading
from dasbus.connection import SessionMessageBus
from dasbus.loop import EventLoop
from usb_dbus import UsbDriver
from usb_driver import init, find_device, usb_reader
import constansts as cons

try:
    dev = find_device()
    init(dev)
except:
    print("Error connecting to USB")
    

print(UsbDriver.__dbus_xml__)

bus = SessionMessageBus()
usb_driver = UsbDriver()
bus.publish_object(cons.PATH, usb_driver)
bus.register_service(cons.DOMEN)

loop = EventLoop()
try:
    loop.run()
except KeyboardInterrupt:
    print('Exiting...')
