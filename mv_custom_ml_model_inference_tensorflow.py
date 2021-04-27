from tensorflow import keras
from tensorflow import expand_dims
import cv2
import time
import datetime
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
    """
    Image classification
    """
    #get ML model for image
    model = keras.models.load_model("your-model.h5") #change here to your model

    #Capture RTSP stream from Cisco Meraki IP Camera, MV12W FPS = 20.0
    cap = cv2.VideoCapture(get_rtspurl(cam_serial)) 
    fps = cap.get(5)
    print("Camera FPS:",fps)

    # Crop the image frame for the ML model if needed
    crop_height = 180
    crop_width = 320
    from_top = 630
    from_left = 346

    while True:
        ret, img = cap.read() #Grabs, decodes and return the next video frame
        #cv2.imshow('my image', img) #alternatively show the output
        cap.set(20,fps) #set the frame with CV_CAP_PROP_POS_FRAMES which needs to be decoded next
        #https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
        #print(cap.get(1))

        crop_img = img[from_top:from_top+crop_height, from_left:from_left+crop_width] #crop image if needed
        crop_img = expand_dims(crop_img, 0) #add one dimension for Keras
        prediction = model.predict(crop_img) #predict on the image frame
        print(prediction) #prints prediction based on your model