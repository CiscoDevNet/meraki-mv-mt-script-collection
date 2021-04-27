import requests
from dateutil import parser
import datetime
import time
import os
import json

meraki_api_key = ""
network_id = ""

def get_snapshot_url_mv_camera(mv_serial, timestamp_iso):
    """
    Get snapshot from specific MV camera at specific time (ISO format)
    (Info: Wait >5 seconds to download images after its generation!)

    Return: Download URL
    """
    headers = {
        "Content-Type": "application/json",
        "X-Cisco-Meraki-API-Key": meraki_api_key
    }
    data = {
        "timestamp" : timestamp_iso
    }
    
    try:
        r_snapshoturl = requests.request('POST', f"https://api.meraki.com/api/v1/devices/{mv_serial}/camera/generateSnapshot", headers=headers, data=json.dumps(data))
        r_snapshoturl_json = r_snapshoturl.json()
        print(f"Got URL for {mv_serial}")
        return r_snapshoturl_json["url"]
    except Exception as e:
        return print(f"Error when getting image URL: {e}")    

def get_snapshot_by_mt_door_event(mt_door_serial, mv_snapshot_camera, num_entries, delta_seconds):
    """
    Download the snapshot images of the Meraki camera when the door sensor is being triggered
    Select MT Door Sensor and the MV Camera where to take the snapshots from + number of events from no

    mt_door_serial: MT serial no
    mv_snapshot_camera: MV serial no
    num_entries: requesting the number of environmental events
    delta_seconds: the delay in seconds when taking the snapshot. Usually 1-2 seconds of delay is better to see the person who is opening the door
    """

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": meraki_api_key
    }
    params = {
        "includedEventTypes[]" : "mt_door",
        "perPage" : num_entries,
        "gatewaySerial" : mt_door_serial
    }
    
    r_envevents = requests.request('GET', f"https://api.meraki.com/api/v1/networks/{network_id}/environmental/events", headers=headers, params=params)
    r_envevents_json = r_envevents.json()


    #Parse events where door was opened and add a timedelta
    #Meraki API: For each timestamp get the snapshot URL and download the image
    for item in r_envevents_json:
        if item["eventData"]["value"] == "1.0":
            print("Getting Snapshot")
            time_plus_delta = parser.parse(item["occurredAt"]) + datetime.timedelta(0,delta_seconds) #delay in seconds
            new_ts_iso = datetime.datetime.isoformat(time_plus_delta)
            new_ts_unix = time_plus_delta.timestamp()

            snapshot_url = get_snapshot_url_mv_camera(mv_snapshot_camera, new_ts_iso)

            time.sleep(5) #wait at least 5 seconds before trying to download the image
            os.makedirs(os.path.dirname(f"images/{mv_snapshot_camera}/"), exist_ok=True) #create folders if not exists

            retries = 0
            success = False
            while success == False:
                try:
                    r_img = requests.get(snapshot_url)
                    if r_img.status_code == 200:
                        with open(f"images/{mv_snapshot_camera}/{new_ts_unix}.jpeg", 'wb') as f:
                            f.write(r_img.content)
                        success = True
                except Exception as e:
                    retries += 1
                    print(f"Error when downloading images: {e}")
                    print(f"Retry: {retries}")
                    time.sleep(30)
                    if retries > 5:
                        print("Error: Avoid endless loop")
                        success = True

if __name__ == "__main__":
    print("Start")
    get_snapshot_by_mt_door_event("xxx-xxx-xxx", "xxx-xxx-xxx", 20, 0) #mt_door_serial, mv_snapshot_camera, num_entries, delta_seconds