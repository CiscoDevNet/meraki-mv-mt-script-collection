import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time
import requests

meraki_api_key = ""
cam_serial = ""


def on_connect(client, userdata, flags, rc):
    """
    The callback for when the client receives a CONNACK response from the server.
    """
    print("Connected with result code "+str(rc))

    # subscribe to each zone's MQTT topic
    for item in zones:
        zoneid = item
        client.subscribe(f"/merakimv/{cam_serial}/{zoneid}")
    client.subscribe(f"/merakimv/{cam_serial}/audio_detections")
    client.subscribe(f"/merakimv/{cam_serial}/audio_analytics")
    client.subscribe(f"/merakimv/{cam_serial}/light")
    #client.subscribe(f"/merakimv/{cam_serial}/raw_detections")


def on_disconnect(client, userdata, flags, rc=0):
    """
    MQTT disconnect
    """
    print("DISconnected with result code "+str(rc))


def on_log(client, userdata, level, buf):
    """
    MQTT logs
    """
    print("log: "+buf)


def on_message(client, userdata, msg):
    """
    The callback for when a PUBLISH message is received from the server.
    """
    data = json.loads(msg.payload.decode('utf-8'))
    split_topic = msg.topic.split("/", 3)
    mqtt_topic = str(split_topic[3])

    # based on the MQTT topic, output the parameters

    if mqtt_topic == "light":
        print("Lux: {}".format(data["lux"]))
    elif mqtt_topic == "audio_analytics":
        print("Audio Level (dB): {}".format(data["audioLevel"]))
    elif mqtt_topic == "audio_detections":
        print("ALARM! {}".format(data[0]["name"]))
    elif mqtt_topic == "raw_detections":
        print("Raw: {}".format(data))
    else:
        try:
            if int(data["counts"]["person"] > 0):
                print("In zone {} are {} person(s).".format(zones[mqtt_topic],data["counts"]["person"]))
        except:
            print(data)

def getzonesinfo(cam_serial):
    """
    Get all zones from the MV camera which are defined by the user in the settings of the Meraki Dashboard
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": meraki_api_key
    }

    try:
        msg = requests.request('GET', f"https://api.meraki.com/api/v1/devices/{cam_serial}/camera/analytics/zones", headers=headers)
        data = msg.json()

        zones = {}

        for item in data:
            if item["zoneId"] != "0":
                zones[item["zoneId"]] = item["label"]
        
        return zones

    except Exception as e:
        print("API Error: {}".format(e))

if __name__ == "__main__":
    print("Getting zones")
    zones = getzonesinfo(cam_serial)

    try:
        print("Start MQTT")
        client = mqtt.Client(client_id="pythonscript",protocol=mqtt.MQTTv311)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        #client.on_log = on_log
        client.on_message = on_message
        client.connect("127.0.0.1", port=1883)

        #run the MQTT connection forever
        client.loop_forever()

    except Exception as e:
        print("MQTT Connection error: {}".format(e))
    