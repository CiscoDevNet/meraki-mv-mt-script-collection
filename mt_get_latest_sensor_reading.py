import requests

meraki_api_key = ""
network_id = ""

def get_latest_sensor_reading(sensor_serial,metric):
	"""
	Get latest sensor reading from MT sensor

	metric: 'temperature', 'humidity', 'water_detection' or 'door'
	"""
	headers = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"X-Cisco-Meraki-API-Key": meraki_api_key
	}

	params = {
		"serials[]" : sensor_serial,
		"metric" : metric
	}

	try:
		msg = requests.request('GET', f"https://api.meraki.com/api/v1/networks/{network_id}/sensors/stats/latestBySensor", headers=headers, params=params)
		if msg.ok:
			data = msg.json()
			return data
	except Exception as e:
		print("API Connection error: {}".format(e))

if __name__ == "__main__":
	print(get_latest_sensor_reading("xxx-xxx-xxx","temperature"))