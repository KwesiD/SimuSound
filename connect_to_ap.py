import requests

url = "http://192.168.4.1/"
while True:
	try:
		res = requests.get(url)
		print(res.content)
	except:
		print("Not connected to SimuSound")

