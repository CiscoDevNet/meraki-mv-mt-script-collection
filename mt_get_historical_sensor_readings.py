import requests

meraki_api_key = ""
network_id = ""

def get_historical_sensor_reading(sensor_serial,metric,timespan,resolution):
	"""
	Get historical sensor readings from MT sensor

	metric: 'temperature', 'humidity', 'water_detection' or 'door'
	timespan: The value must be in seconds and be less than or equal to 730 days. The default is 2 hours.
	resolution: The valid resolutions are: 1, 120, 3600, 14400, 86400. The default is 120.
	"""
	headers = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"X-Cisco-Meraki-API-Key": meraki_api_key
	}

	params = {
		"serials[]" : sensor_serial,
		"metric" : metric,
		"timespan" : timespan,
		"resolution" : resolution,
		"agg" : "avg"
	}

	try:
		msg = requests.request('GET', f"https://api.meraki.com/api/v1/networks/{network_id}/sensors/stats/historicalBySensor", headers=headers, params=params)
		if msg.ok:
			data = msg.json()
			return data
	except Exception as e:
		print("API Connection error: {}".format(e))

if __name__ == "__main__":
	#print(get_historical_sensor_reading("xxx-xxx-xxx","temperature",2592000,3600))   #last 30 days, sensor reading every 60 min
	#print(get_historical_sensor_reading("xxx-xxx-xxx","humidity",2592000,3600))   #last 30 days, sensor reading every 60 min
	#print(get_historical_sensor_reading("xxx-xxx-xxx","door",86400,120))             #last day, sensor reading every 2 min
	#print(get_historical_sensor_reading("xxx-xxx-xxx","water_detection",86400,120))  #last day, sensor reading every 2 min