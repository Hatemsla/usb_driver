# usb_driver.py

import threading
import usb.core
import constansts as cons

dtr = False
rts = False
dev = None
ret = None
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
    dev = usb.core.find()
    if dev is None:
        raise ValueError('Device not found')

    print(dev)

    return dev

def init(dev):
    global ret
    print("init")

    # checkState("init #1", 0x5f, 0, new int[]{-1 /* 0x27, 0x30 */, 0x00});
    ret = control_read(dev, cons.VENDOR_VERSION, 0, 0, 0x02)
    print("VENDOR_VERSION ret=", ret, to_hex(ret))

    # if (controlOut(0xa1, 0, 0) < 0) {
    ret = control_write(dev, cons.VENDOR_SERIAL_INIT, 0, 0, 0x00)
    print("SERIAL_INIT ret=", ret, to_hex(ret))

    set_baud_rate(dev, cons.DEFAULT_BAUD_RATE)

    # checkState("init #4", 0x95, 0x2518, new int[]{-1 /* 0x56, c3*/, 0x00});
    ret = control_read(dev, cons.VENDOR_READ, 0x2518, 0, 0x00)
    print("VENDOR_WRITE.1 ret=", ret, to_hex(ret))

    # controlOut(0x9a, 0x2518, LCR_ENABLE_RX | LCR_ENABLE_TX | LCR_CS8)
    ret = control_write(dev, cons.VENDOR_WRITE, 0x2518, cons.LCR_ENABLE_RX | cons.LCR_ENABLE_TX | cons.LCR_CS8, 0x00)
    print("VENDOR_WRITE.3 ret=", ret, to_hex(ret))

    # checkState("init #6", 0x95, 0x0706, new int[]{-1/*0xf?*/, -1/*0xec,0xee*/});
    ret = control_read(dev, cons.VENDOR_READ, 0x0706, 0, 0x00)
    print("VENDOR_WRITE.1 ret=", ret, to_hex(ret))

    # controlOut(0xa1, 0x501f, 0xd90a)
    ret = control_write(dev, cons.VENDOR_SERIAL_INIT, 0x501f, 0xd90a, 0x00)
    print("VENDOR_SERIAL_INIT.3 ret=", ret, to_hex(ret))

    set_baud_rate(dev, cons.DEFAULT_BAUD_RATE)

    set_control_lines(dev)


def set_control_lines(dev):
    global ret
    ret = control_write(dev, cons.VENDOR_MODEM_OUT, ~((dtr and cons.SCL_DTR or 0) | (rts and cons.SCL_RTS or 0)), 0, 0x00)
    print("set_control_lines ret=", ret)

    return ret

def set_baud_rate(dev, baudRate):
    global ret
    print("set_baud_rate")

    factor: int
    divisor: int

    if (baudRate == 921600):
        divisor = 7
        factor = 0xf300
    else:
        BAUDBASE_FACTOR = 1532620800
        BAUDBASE_DIVMAX = 3

        factor = int(BAUDBASE_FACTOR / baudRate)
        divisor = BAUDBASE_DIVMAX

        while ((factor > 0xfff0) and divisor > 0):
            factor >>= 3
            divisor=divisor-1
        
        assert factor < 0xfff0

        factor = 0x10000 - factor

    divisor |= 0x0080

    print("factor", factor)

    val1 = (int) ((factor & 0xff00) | divisor)
    val2 = (int) (factor & 0xff)

    print("baud rate=%d, 0x1312=0x%04x, 0x0f2c=0x%04x".format(baudRate, val1, val2))

    ret = control_write(dev, cons.VENDOR_WRITE, 0x1312, val1, 0x00)
    print("VENDOR_WRITE.BaudDate.1 ret=", ret)

    ret = control_write(dev, cons.VENDOR_WRITE, 0x0f2c, val2, 0x00)
    print("VENDOR_WRITE.BaudDate.2 ret=", ret)


def control_write(dev, req, index, value, data):
    global ret
    print("control_write")
    ret = dev.ctrl_transfer(cons.VENDOR_WRITE_TYPE, req, index, value, data)
    return ret

def control_read(dev, req, index, value, len):
    global ret
    print("control_read")
    ret = dev.ctrl_transfer(cons.VENDOR_READ_TYPE, req, index, value, len)
    return ret 

def send_hello(dev, msg):
    global ret
    print("Send message ", msg)
    ret = dev.write(cons.WRITE_PORT, msg, cons.USB_TIMEOUT_MILLIS)
    print("Write ret=", ret)
    return ret

def to_hex(ret):
    if (isinstance(ret, int)):
        return '0x{:02x} '.format(ret)
    else:    
        return ''.join('0x{:02x} '.format(x) for x in ret)