from bluepy import btle
import struct, os
from concurrent import futures
import time

global addr_var
global delegate_global
global perif_global
global temp_global

addr_var = ['ec:24:b8:1d:d6:88', 'c8:fd:19:13:a0:76', '18:93:D7:31:BE:40']
delegate_global = [0] * len(addr_var)
perif_global = [0] * len(addr_var)
temp_global = [0] * len(addr_var)


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global addr_var
        global delegate_global
        global temp_global

        for ii in range(len(addr_var)):
            if delegate_global[ii] == self:
                try:
                    data_decoded = struct.unpack("b", data)
                    perif_global[ii].writeCharacteristic(cHandle, struct.pack("b", 55))
                    print("Address: " + addr_var[ii])
                    print(data_decoded)
                    return
                except:
                    pass
                try:
                    data_decoded = data.decode('utf-8')
                    perif_global[ii].writeCharacteristic(cHandle, struct.pack("b", 55))

                    s_data = str(data_decoded)
                    splited = s_data.split(':')
                    temp_global[ii] = int(splited[4])
                    print("Address: " + addr_var[ii])
                    print(data_decoded)
                    print(time.time())
                    return
                except:
                    pass


def perif_loop(perif, indx):
    services = perif.getServices()
    s = perif.getServiceByUUID(list(services)[2].uuid)
    c = s.getCharacteristics()[0]
    while True:
        try:
            if perif.waitForNotifications(1.0):
                print("waiting for notifications...")
                continue
            now_temp = temp_global[indx]
            if now_temp < 20:
                c.write(bytes("of".encode()))
            else:
                c.write(bytes("on".encode()))

        except:
            try:
                perif.disconnect()
            except:
                pass
            print(f"disconnecting perif : {perif.addr}, index {indx}")
            reestablish_connection(perif, perif.addr, indx)


# [delegate_global.append(0) for ii in range()]
# [perif_global.append(0) for ii in range(len(addr_var))]


def reestablish_connection(perif, addr, indx):
    while True:
        try:
            print("trying to reconnect with " + addr)
            perif.connect(addr)
            print(f"re-connected to {addr}, indx = {indx}")
            return
        except:
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
        except:
            print("failed to connect to " + addr)
            continue


ex = futures.ProcessPoolExecutor(max_workers=os.cpu_count())
results = ex.map(establish_connection, addr_var)
