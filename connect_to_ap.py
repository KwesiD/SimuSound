import requests
import json 

url = "http://192.168.4.1/"
payload = {"ssid":"Test"}
while True:
	try:
		res = requests.post(url,data=json.dumps(payload))
		print(res.content)
	except:
		print("Not connected to SimuSound")

