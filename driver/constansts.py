# constants.py

DOMEN = "org.usb.UsbDriver"
PATH = "/org/usb/UsbDriver"

READ_PORT = 0x82
WRITE_PORT = 0x02
PACKAGE_SIZE = 1024

USB_TIMEOUT_MILLIS = 1000

VENDOR_WRITE_TYPE  = 0x40
VENDOR_READ_TYPE   = 0xC0

VENDOR_READ	       = 0x95
VENDOR_WRITE       = 0x9A
VENDOR_SERIAL_INIT = 0xA1
VENDOR_MODEM_OUT   = 0xA4
VENDOR_VERSION     = 0x5F

LCR_ENABLE_RX   = 0x80
LCR_ENABLE_TX   = 0x40
LCR_MARK_SPACE  = 0x20
LCR_PAR_EVEN    = 0x10
LCR_ENABLE_PAR  = 0x08
LCR_STOP_BITS_2 = 0x04
LCR_CS8         = 0x03
LCR_CS7         = 0x02
LCR_CS6         = 0x01
LCR_CS5         = 0x00

GCL_CTS = 0x01
GCL_DSR = 0x02
GCL_RI  = 0x04
GCL_CD  = 0x08
SCL_DTR = 0x20
SCL_RTS = 0x40

DEFAULT_BAUD_RATE = 115200