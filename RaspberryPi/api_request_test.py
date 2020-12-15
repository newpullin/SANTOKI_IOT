import requests, json

IP = 'Your IP'
PORT = 'Your Port'

param1 = {"mac_addr": ["MAC1", "MAC2"]}

res1 = requests.post(f"http://{IP}:{PORT}/isregistered", data=json.dumps(param1))


def get_result(res):
    if res.request:
        print(res.status_code)
        print(res.json())


get_result(res1)


