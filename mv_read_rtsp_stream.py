import cv2
import time
import requests

meraki_api_key = ""
cam_serial = ""

def get_rtspurl(cam_serial):
    """
    Get RTSP URL from camera
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": meraki_api_key
    }

    try:
        r_rtspurl = requests.request('GET', f"https://api.meraki.com/api/v1/devices/{cam_serial}/camera/video/settings", headers=headers)
        r_rtspurl_json = r_rtspurl.json()
        return r_rtspurl_json["rtspUrl"]
    except Exception as e:
        return print(f"Error when getting image URL: {e}") 

if __name__ == "__main__":
    print("Start")
    cap = cv2.VideoCapture(get_rtspurl(cam_serial)) 
    print("Camera FPS: ", cap.get(5))

    if cap.isOpened() == False:
        print("Streaming Error! Wrong URL?")

    # While the video is opened
    while cap.isOpened():

        # Read video file
        ret, frame = cap.read()

        if ret == True:
            cv2.imshow('My MV Camera', frame)

            # Press q to quit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()