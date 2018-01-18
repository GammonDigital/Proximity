from bluepy.btle import Scanner, DefaultDelegate
import RPi.GPIO as GPIO

beaconAddr = ["c8:03:83:4f:aa:42"]
beaconThreshold = -40

# GPIO preset TODO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

# Init alarm state
alarm = False
counter = 0

# Def alarm on/off TODO
def alarmOn():
    GPIO.output(7,True)
            
def alarmOff():
    GPIO.output(7,False)
    
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

# Continuous scan
while True:
    try:
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(0.5) # Scans for n seconds
        beaconRssiList = []
        for dev in devices:
            if (beaconAddr in dev.addr):
                print("Device {}, RSSI={} dB".format(dev.addr, dev.rssi))
                beaconRssiList.append(dev.rssi)
        if (max(beaconRssiList, default=-999)>beaconThreshold):
            if alarm == False:
                counter = 0
                alarmOn()
                alarm = True
        elif (not beaconRssiList) or (max(beaconRssiList) < beaconThreshold):
            counter += 1
            if counter > 25:
                counter = 0
                alarmOff()
                alarm = False
    except (KeyboardInterrupt) as k:
        GPIO.cleanup()
        quit()
    except (IOError, EOFError, TimeoutError) as e:
        GPIO.cleanup()
