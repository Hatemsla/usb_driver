# usb_driver.py

import threading
import usb.core
import usb.backend.openusb
import constansts as cons

dtr = False
rts = False
dev = None
ret = None
ep_read = None
ep_write = None
ret_lock = threading.Lock()

def usb_reader(dev):
    global ret
    while True:
        try:
            new_data = dev.read(cons.READ_PORT, cons.PACKAGE_SIZE, cons.USB_TIMEOUT_MILLIS)
            # print(str(new_data, 'cp1251'))
            with ret_lock:
                ret = new_data
                # print(str(ret, 'cp1251'))
        except Exception as e:
            print(f"Error reading from USB: {e}")

def find_device():
    global dev
    devs = usb.core.find(find_all=True)
    if devs is None:
        raise ValueError('Device not found')

    print("All devs")
    for d in devs:
        if d.idVendor == 0x0483 and d.idProduct == 0x5740:
            dev = d
        elif d.idVendor == 0x1e4e and d.idProduct == 0x0110:
            dev = d
        elif d.idVendor == 0x046d and d.idProduct == 0x0892:
            dev = d
        elif d.idVendor == 0x1a86 and d.idProduct == 0x7523:
            dev = d
        print(d)

    print('target dev', dev, sep='\n')

    return dev

def init(dev):
    global ret, ep_read, ep_write
    print("init")
    
    try:
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)
    except Exception as e:
        print(e)
        print("Error detaching kernel driver")
        return e
    
    try:
        dev.reset()
    except Exception as e:
        print(e)
        print("Error resetting device")
        return e

    # try:
    #     dev.set_configuration()
    # except Exception as e:
    #     print(e)
    #     print("Error setting configuration")
    #     return e
    
    try:
        cfg = dev.get_active_configuration()
        print(cfg)
        intf = cfg[(0, 0)]
        for cf in cfg:
            print(cf.bInterfaceNumber)
            if cf.bInterfaceNumber != 0 and cf.bAlternateSetting == 0xb:
                print("\n\nintf")
                print(cf)
                intf = cf
                break
    except Exception as e:
        print(e)
        print("Error getting configuration")
        return e
    
    try:
        ep_read = usb.util.find_descriptor(
            intf,
            custom_match= \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_IN)
    except Exception as e:
        print(e)
        print("Error finding IN endpoint")
        return e
        
    try:
        ep_write = usb.util.find_descriptor(
            intf,
            custom_match= \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT)
    except Exception as e:
        print(e)
        print("Error finding OUT endpoint")
        return e