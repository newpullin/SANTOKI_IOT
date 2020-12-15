from bluepy import btle


class ScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device , {dev.addr}")
        elif isNewData:
            print("Received new data from ", dev.addr)


scanner = btle.Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    print(f"Device {dev.addr} ({dev.addrType}) , RSSI={dev.rssi}")
    for (adtype, desc, value) in dev.getScanData():
        print(f"{desc} = {value}")
