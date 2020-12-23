import pyrebase

config = {
    ""
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

devices = db.child("devices").get()

for x in devices.each():
	print(x.key(), x.val()['hub_mac'])
print(devices)
