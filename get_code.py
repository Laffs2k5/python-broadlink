"""Helper script for auto capture"""
import time
import binascii
import broadlink

# config
IP_OF_DEVICE = '192.168.0.155'
COMMAND_MAX_LEARNTIME_SEC=10

# "Main"
def start_capture():
    """Start capture of IR codes"""
    devices = broadlink.discover(timeout=5)
    print str(len(devices)) + " devices found, looking for " + IP_OF_DEVICE + "..."
    device = (([dev for dev in devices if dev.host[0] == IP_OF_DEVICE])[:1] or [None])[0]
    if device is not None:
        device.auth()

        print "found. Learning from device:"
        print "             ip:  " + device.host[0]
        print "           port:  " + str(device.host[1])
        mac = binascii.hexlify(device.mac)[::-1]
        print "  broadlink mac:  0x" + ''.join([mac[i:i+2] for i in range(0, len(mac), 2)])
        mac = binascii.hexlify(device.mac)
        print "        std mac:  " + ':'.join([mac[i-2:i] for i in range(2, len(mac)+2, 2)][::-1])
        #print "     key:\t" + binascii.hexlify(device.key)
        print "            key:  097628343fe99e23765c1513accf8b02"
        #print "      iv:\t" + binascii.hexlify(device.iv)
        print "             iv:  562e17996d093d28ddb3ba695a2e6f58"

        while True:
            device.enter_learning()
            print "\nSend IR now"
            time.sleep(COMMAND_MAX_LEARNTIME_SEC)
            ir_packet = []
            ir_packet = device.check_data()
            if ir_packet is not None:
                device.send_data(ir_packet)
                inp = raw_input(str(len(ir_packet)) + ', accept?\n')
                if inp[0] in ['y', 'Y']:
                    try:
                        print binascii.hexlify(ir_packet)
                    except:
                        pass
            else:
                break
    elif devices is not None:
        print "No devices had ip: " + IP_OF_DEVICE
    return

start_capture()
