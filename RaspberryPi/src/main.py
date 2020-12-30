from bluepy import btle
import requests, json

from raspy_config import *
import struct, os

from concurrent import futures
import time
import time
import pyrebase
from datetime import datetime
from influxdb import InfluxDBClient


    
# Connect Wifi by Bluetooth , skip




# add queryn by d-box mac address needed
print("get data from DB...")

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)

db = firebase.database()

devices_db = db.child("devices").get()

print("DB data loaded!")

# scan bluetooth
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



# get list of my sensor
devices_addr = []
for dev in devices:
	print(f"Device {dev.addr} ({dev.addrType}) , RSSI={dev.rssi}")
	devices_addr.append(dev.addr)
	

print(devices_addr)

# registered_mac_list = requests.post(f"http://{REGISTERED_CHECKING_IP}:{REGISTERED_CHECKING_PORT}/isregistered", data=json.dumps(mac_param)).json()['registered']
# print(registered_mac_list)



global addr_var
global delegate_global
global perif_global

addr_key = []
addr_var = []
addr_last = []
influx_last = []



# influx db client
client = InfluxDBClient(host=INFLUXDB_IP, port=INFLUXDB_PORT)
client.get_list_database()
client.switch_database(INFLUXDB_NAME)

print("select registered device")
for device in devices_db.each():
	if device.val()['device_type'] == 'dbox':
		continue
	
	mac_addr = device.val()['mac'].lower()
	diff = 0
	if  mac_addr in devices_addr :
		addr_var.append(mac_addr)
		addr_last.append(device.val()['last_update'] + diff)
		addr_key.append(device.key())
		influx_last.append(int(time.time()) + diff)
		diff += 1
		
print(addr_key)
print(addr_var)

delegate_global = [0] * len(addr_var)
perif_global = [0] * len(addr_var)
temp_global = [0] * len(addr_var)
class MyDelegate(btle.DefaultDelegate):
	def __init__(self, params):
		btle.DefaultDelegate.__init__(self)
	def handleNotification(self, cHandle, data):
		global addr_var
		global delegate_global
		for ii in range(len(addr_var)):
			if delegate_global[ii]==self:
				try:
					data_decoded = data.decode('utf-8')
					perif_global[ii].writeCharacteristic(cHandle, struct.pack("b", 55))
					s_data = str(data_decoded)
					# s_data = 0:humidity:h_value:temperature:t_value
					splited = s_data.split(':')
					temp_global[ii] = int(splited[4])
					now_time = int(time.time())
					if now_time - addr_last[ii] > 3600:
						addr_last[ii] = now_time
						try :
							db.child("devices").child(addr_key[ii]).update({"temperature":str(int(splited[4])), "last_update" : now_time, "humidity":str(int(splited[2]))})
							print("update firebase db success..")
						except:
							print("update firebase db failed..")
					if now_time - influx_last[ii] > 60:
						influx_last[ii] = now_time
						json_body = [{"measurement": "TH", "tags" : { "mac" : addr_var[ii] }, "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "fields" : {"temperature":int(splited[4]),"humidity":int(splited[2])}}]
						
						if client.write_points(json_body):
							print("insert influxdb Success")
						
						
					print(f"{datetime.now().strftime('%H:%M:%SZ')} Address: {addr_var[ii]} {data_decoded}" )
					return
				except :
					pass


def perif_loop(perif, indx):
	services = perif.getServices()
	s = perif.getServiceByUUID(list(services)[2].uuid)
	c = s.getCharacteristics()[0]
	while True:
		try:
			if perif.waitForNotifications(1.0):
				continue
			now_temp = temp_global[indx]
			if now_temp < 20:
				c.write(bytes("of".encode()))
			else:
				c.write(bytes("on".encode()))

		except :
			try:
				perif.disconnect()
			except :
				pass
			print(f"disconnecting perif : {perif.addr}, index {indx}")
			reestablish_connection(perif, perif.addr, indx)


#[delegate_global.append(0) for ii in range()]
#[perif_global.append(0) for ii in range(len(addr_var))]


def reestablish_connection(perif, addr, indx):
    while True:
        try:
            print("trying to reconnect with " + addr)
            perif.connect(addr)
            print(f"re-connected to {addr}, indx = {indx}")
            return
        except :
            continue


def establish_connection(addr):
    global delegate_global
    global perif_global
    global addr_var

    while True:
        try:
            for jj in range(len(addr_var)):
                if addr_var[jj] == addr:
                    print(f"Attempting to connect with {addr} at index : {jj}")
                    p = btle.Peripheral(addr)
                    perif_global[jj] = p
                    p_delegate = MyDelegate(addr)
                    delegate_global[jj] = p_delegate
                    p.withDelegate(p_delegate)
                    perif_loop(p, jj)
        except :
            print("failed to connect to " + addr)
            continue


ex = futures.ProcessPoolExecutor(max_workers=os.cpu_count())
results = ex.map(establish_connection, addr_var)



