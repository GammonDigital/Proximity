from bluepy.btle import Scanner, DefaultDelegate
import csv
import RPi.GPIO as GPIO

# Variables
try:
    with open('/home/pi/Documents/Proximity_Detection/beaconReg.csv', 'r') as f:  # Import registered beacons
        beaconListFull = list(csv.reader(f))
        beaconAddr = [item[1] for item in beaconListFull]
    with open('/home/pi/Documents/Proximity_Detection/threshold.txt', 'r') as g:
        beaconThreshold = int(g.readline())
except (IOError, EOFError, TimeoutError) as e:
        GPIO.cleanup()

# GPIO preset
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

# Init alarm state
alarm = False
counter = 0

# Def alarm on/off
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
        devices = scanner.scan(2) # Scans for n seconds
        beaconRssiList = []
        for dev in devices:
            if (dev.addr in beaconAddr):
                print("Device {}, RSSI={} dB".format(dev.addr, dev.rssi))
                beaconRssiList.append(dev.rssi)
        if (max(beaconRssiList, default=-999)>beaconThreshold):
            if alarm == False:
                counter = 0
                alarmOn()
                alarm = True
        elif (not beaconRssiList) or (max(beaconRssiList) < beaconThreshold):
            counter += 1
            if counter > 2:
                counter = 0
                alarmOff()
                alarm = False
    except (KeyboardInterrupt) as k:
        GPIO.cleanup()
        quit()
    except (IOError, EOFError, TimeoutError) as l:
        GPIO.cleanup()
