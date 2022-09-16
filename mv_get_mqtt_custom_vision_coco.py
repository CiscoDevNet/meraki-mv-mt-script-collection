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

    client.subscribe(f"/merakimv/{cam_serial}/custom_analytics")


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

    # print Coco object class
    # https://github.com/nightrome/cocostuff/blob/master/labels.txt
    for coco_class in data["outputs"]:
        print(coco_class["class"])

if __name__ == "__main__":

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
    