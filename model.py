 
import cv2
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
from centroidtracker import CentroidTracker
import json
import requests
import RPi.GPIO as GPIO
from time import sleep
from pyzbar.pyzbar import decode

# Makes program run headlessly
# matplotlib.use('Agg')

# GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Individual Motor class
class Motor():
    def __init__(self,Ena,In1,In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.Ena, 100)
        self.pwm.start(0)
    
    def Forward(self, time=0.2):
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(30)
        sleep(time)
        
    def Stop(self, time=0.2):
        self.pwm.ChangeDutyCycle(0)
        sleep(time)
        

# Group Motors movement functions
def Left(motor1, motor2, motor3, motor4):
    print('Left')
    motor1.Stop()
    motor2.Stop()
    motor3.Forward()
    motor4.Forward()

def Right(motor1, motor2, motor3, motor4):
    print('Right')
    motor1.Forward()
    motor2.Forward()
    motor3.Stop()
    motor4.Stop()
    
def Forward(motor1, motor2, motor3, motor4):
    print('Forward')
    motor1.Forward()
    motor2.Forward()
    motor3.Forward()
    motor4.Forward()

def Stop(motor1, motor2, motor3, motor4):
    print('Stop')
    motor1.Stop()
    motor2.Stop()
    motor3.Stop()
    motor4.Stop()

# Configuring motor objects
motor1 = Motor(2,3,4)
motor2 = Motor(17,27,22)
motor3 = Motor(10,9,11)
motor4 = Motor(5,6,13)

# Pre-trained model setup
config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'frozen_inference_graph.pb'

# Create model object
model = cv2.dnn_DetectionModel(frozen_model,config_file)

classLabels = []
file_name = 'labels.txt'
# Create list of labels from file
with open(file_name,'rt') as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')

# Create tracker object
tracker = CentroidTracker(maxDisappeared=80, maxDistance=90)

# Set model configuration
model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5,127.5,127.5))
model.setInputSwapRB(True)

# Read video
video = cv2.VideoCapture(0)
if not video.isOpened():
    video = cv2.VideoCapture(0)
if not video.isOpened():
    raise IOError('Cannot Open Video')

# Font definitions
font_scale = 3
font = cv2.FONT_HERSHEY_PLAIN

# Function used to process video feed and determine movement commands to pi
def Movement(center):
    if(center[0] < 200):
        print('Left')
    if(center[0] > 400):
        print('Right')
    if(center[1] > 340):
        print('Forward')
    if(center[1] < 140):
        print('Stop')

Enable = 1
def GetEnableStatus():
    url = "http://192.168.1.8:3000/EnableStatus"
    response = requests.get(url)
    data = response.json()
    Enable = data['Enable']
    print(Enable)

def SendItemData(Type, Price):
    url = "http://192.168.1.8:3000"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    message = {'Type': Type, 'Price': Price}
    response = requests.post(url, data=json.dumps(message), headers=headers)

# Open Source Function used to remove noise from detections
def non_max_suppression_fast(boxes, overlapThresh):
    try:
        if len(boxes) == 0:
            return []

        if boxes.dtype.kind == "i":
            boxes = boxes.astype("float")

        pick = []

        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(y2)

        while len(idxs) > 0:
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)

            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.minimum(x2[i], x2[idxs[:last]])
            yy2 = np.minimum(y2[i], y2[idxs[:last]])

            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            overlap = (w * h) / area[idxs[:last]]

            idxs = np.delete(idxs, np.concatenate(([last],
                                                   np.where(overlap > overlapThresh)[0])))

        return boxes[pick].astype("int")
    except Exception as e:
        print("Exception occurred in non_max_suppression : {}".format(e))

# Run while enable from app is recieved
while Enable:
    
    # Configure frame
    ret, frame = video.read()
    cv2.line(frame, pt1=(400,0), pt2=(400,600), color=(0,0,255), thickness=5)
    cv2.line(frame, pt1=(200,0), pt2=(200,600), color=(0,0,255), thickness=5)
    cv2.line(frame, pt1=(0,340), pt2=(600,340), color=(0,0,255), thickness=5)
    cv2.line(frame, pt1=(0,140), pt2=(600,140), color=(0,0,255), thickness=5)
    #height, width, _ = frame.shape
    #print(height, width)
    
    #Detect and Read barcode
    for barcode in decode(frame):
        # Convert barcode to string
        Data = barcode.data.decode('utf-8')
        #print(Data)
        data = Data.split("-", 1)
        #print(data[0])
        #print(data[1])
        SendItemData(data[0], data[1])
        # Draw box around barcodes
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame, [pts], True, (255,0,255), 5)
        
    # Call model
    ClassIndex, confidence, bbox = model.detect(frame, confThreshold=0.5)

    # List to store coordinates of bounding boxes
    rects = []
    # Check something has been detected in the frame
    if (len(ClassIndex)!=0):
        # Removing double brackets and adding boxes
        for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
            # Check if person is detected
            if (ClassInd == 1):
                center = (math.floor((boxes[0]+boxes[2])/2), math.floor((boxes[1]+boxes[3])/2))
                #print(center)
                #cv2.circle(frame, center, 3, (0,0,255), 2)
                #Movement(center, 0)
                #cv2.rectangle(frame,boxes,(255, 0, 0), 2)
                #cv2.putText(frame,classLabels[ClassInd-1],(boxes[0]+10,boxes[1]+40), font, fontScale=font_scale,color=(0, 255, 0), thickness=3)
                rects.append(boxes)

        boundingBoxes = np.array(rects)
        boundingBoxes = boundingBoxes.astype(int)
        rects = non_max_suppression_fast(boundingBoxes, 0.3)
        
        # Send bounding boxes to tracker
        objects = tracker.update(rects)
        # Extracting and displaying ObjectId
        for (objectId, bbox) in objects.items():
            x1,y1,x2,y2 = bbox
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)

            if(objectId == 0):
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)
                text = "ID: {}".format(objectId)
                cv2.putText(frame, text, (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)
                cv2.circle(frame, center, 3, (0,0,255), 2)
                Movement(center)
                #sleep(2)

    # Display video
    cv2.imshow('Object Detection',frame)
    
    # Cancel video playback if 'q' key is pressed
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
