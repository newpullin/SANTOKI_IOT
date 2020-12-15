from bluepy import btle
import struct
import time

# global temp
temp = 0
# global temp_prev
temp_prev = 0


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        ##        print(self)
        ##        print(cHandle)
        # print(struct.unpack("b",data))
        s_data = str(data)
        s_data = s_data[2:len(s_data) - 1]
        splited = s_data.split(':')
        global temp
        temp = float(splited[4])
        print(temp)


p = btle.Peripheral('C8:FD:19:13:A0:76')
p.setDelegate(MyDelegate(0))

services = p.getServices()
s = p.getServiceByUUID(list(services)[2].uuid)
c = s.getCharacteristics()[0]

# displays all services
# for service in services:
#   print (service)


# get uuid
"""
chList = p.getCharacteristics()
print("Handle   UUID                                Properties")
print("-------------------------------------------------------" )                
for ch in chList:
   print("  0x"+ format(ch.getHandle(),'02X')  +"   "+str(ch.uuid) +" " + ch.propertiesToString())
"""

"""
Handle   UUID                                Properties
-------------------------------------------------------
  0x03   00002a00-0000-1000-8000-00805f9b34fb READ 
  0x05   00002a01-0000-1000-8000-00805f9b34fb READ 
  0x07   00002a02-0000-1000-8000-00805f9b34fb READ WRITE 
  0x09   00002a03-0000-1000-8000-00805f9b34fb WRITE 
  0x0B   00002a04-0000-1000-8000-00805f9b34fb READ 
  0x0E   00002a05-0000-1000-8000-00805f9b34fb INDICATE 
  0x12   0000ffe1-0000-1000-8000-00805f9b34fb READ WRITE NO RESPONSE WRITE NOTIF
"""

"""

#get name

dev_name_uuid = btle.UUID(0x2A00)
ch = p.getCharacteristics(uuid=dev_name_uuid)[0];
if(ch.supportsRead()):
	print(ch.read())

b'arduiono'

time.sleep(2)
led_service_uuid = btle.UUID(0x002A00)
led_char_uuid = btle.UUID(0x002A03)

LedService = p.getServiceByUUID(led_service_uuid)

ch = LedService.getCharacteristics(led_char_uuid)[0]
"""

while True:
    if p.waitForNotifications(1.0):
        continue
    print("waiting...")

    if temp < 20:
        c.write(bytes("of".encode()))
    else:
        c.write(bytes("on".encode()))

