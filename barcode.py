
# Program for detecting and reading barcodes
import cv2
import numpy as np
#from pyzbar.pyzbar import decode
import requests
import json

video = cv2.VideoCapture(0)

# Set width and height of camera frame
width = 3
height = 4
video.set(width,640)
video.set(height,480)

url = "http://localhost:3000"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def SendData(Type, Price):
    #message = {'msg': 'Milk, $4.00'}
    message = {'Type': Type, 'Price': Price}
    response = requests.post(url, data=json.dumps(message), headers=headers)

#while True:

    #success, img = video.read()
    #for barcode in decode(img):
        # Convert barcode to string
        #Data = barcode.data.decode('utf-8')
    #    print(Data)
        # Draw box around barcodes
    #    pts = np.array([barcode.polygon], np.int32)
    #    pts = pts.reshape((-1,1,2))
    #    cv2.polylines(img, [pts], True, (255,0,255), 5)
SendData('Butter', 4.5)
SendData('Milk', 6)

    #cv2.imshow('Result', img)
    #cv2.waitKey(1)