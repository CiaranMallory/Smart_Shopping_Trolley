
import cv2
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
import json
import requests
import RPi.GPIO as GPIO
from time import sleep
from pyzbar.pyzbar import decode
import multiprocessing

serverIP = ''
#matplotlib.use('Agg')

# GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Function to draw box around person
def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)

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

tracker = cv2.legacy.TrackerMOSSE_create()
#tracker = cv2.legacy.TrackerKCF_create()

# Font definitions
font_scale = 3
font = cv2.FONT_HERSHEY_PLAIN

# Function used to process video feed and send movement commands to pi
def Movement(center):
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
            self.pwm.ChangeDutyCycle(100)
            sleep(time)
            
        def Stop(self, time=0.2):
            self.pwm.ChangeDutyCycle(0)
            sleep(time)
            

    # Group Motors movement functions
    def Left(motor1, motor2, motor3, motor4):
        #print('Left')
        motor1.Stop()
        motor2.Stop()
        motor3.Forward()
        motor4.Forward()

    def Right(motor1, motor2, motor3, motor4):
        #print('Right')
        motor1.Forward()
        motor2.Forward()
        motor3.Stop()
        motor4.Stop()
        
    def Forward(motor1, motor2, motor3, motor4):
        #print('Forward')
        motor1.Forward()
        motor2.Forward()
        motor3.Forward()
        motor4.Forward()

    def Stop(motor1, motor2, motor3, motor4):
        #print('Stop')
        motor1.Stop()
        motor2.Stop()
        motor3.Stop()
        motor4.Stop()

    # Configuring motor objects
    motor1 = Motor(2,3,4)
    motor2 = Motor(17,27,22)
    motor3 = Motor(10,9,11)
    motor4 = Motor(25,8,7)
    
    if(center[0] < 200):
        print('Left')
        Right(motor1, motor2, motor3, motor4)
        sleep(0.5)
        Stop(motor1, motor2, motor3, motor4)
    if(center[0] > 400):
        print('Right')
        Left(motor1, motor2, motor3, motor4)
        sleep(0.5)
        Stop(motor1, motor2, motor3, motor4)
    if(center[1] > 250):
        print('Forward')
        Forward(motor1, motor2, motor3, motor4)
        sleep(0.5)
        Stop(motor1, motor2, motor3, motor4)
    if(center[1] < 140):
        print('Stop')
        Stop(motor1, motor2, motor3, motor4)
        sleep(0.5)
        Stop(motor1, motor2, motor3, motor4)

Enable = 1
def GetEnableStatus():
    url = "http://${serverIP}:3000/EnableStatus"
    response = requests.get(url)
    data = response.json()
    Enable = data['Enable']
    print(Enable)

def SendItemData(Type, Price):
    url = "http://${serverIP}:3000"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    message = {'Type': Type, 'Price': Price}
    response = requests.post(url, data=json.dumps(message), headers=headers)

# Count variable to prevent Movement function being called to frequent
count = 0

while True:
    try:
        if(Enable):
            # Configure frame
            ret, frame = video.read()

            # Call model to detect user
            ClassIndex, confidence, bbox = model.detect(frame, confThreshold=0.5)

            # Check something has been detected in the frame
            if (len(ClassIndex)!=0):
                # Removing double brackets and adding boxes
                for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
                    # Check if person is detected
                    if (ClassInd == 1):
                        # Start tracking the person
                        tracker.init(frame,boxes)
                        
                        while True:

                            success, frame = video.read()
                            success, bbox = tracker.update(frame)
                            #print(bbox)

                            if success:
                                drawBox(frame,bbox)
                                #center = (math.floor((bbox[0]+bbox[2])/2), math.floor((bbox[1]+bbox[3])/2))
                                # center = ((x + width/2), (y+height/2))
                                center = (math.floor(bbox[0]+(bbox[2])/2), math.floor(bbox[1]+(bbox[3])/2))
                                cv2.circle(frame, center, 3, (0,0,255), 2)
                                process1 = multiprocessing.Process(target=Movement, args=(center,))
                                #print(center)
                                #cv2.circle(frame, center, 3, (0,0,255), 2)
                                if (count == 10):
                                    #Movement(center)
                                    process1.start()
                                    #process1.join()
                                    count = 0
                                count+=1
                                
                            # Detect and Read barcode
                            for barcode in decode(frame):
                                # Convert barcode to string
                                Data = barcode.data.decode('utf-8')
                                #print(Data)
                                data = Data.split("-", 1)
                                #print(data[0])
                                #print(data[1])
                                #SendItemData(data[0], data[1])
                                # Draw box around barcodes
                                pts = np.array([barcode.polygon], np.int32)
                                pts = pts.reshape((-1,1,2))
                                cv2.polylines(frame, [pts], True, (255,0,255), 5)

                            # Display video
                            cv2.imshow('Object Detection',frame)
                            
                            # Cancel video playback if 'q' key is pressed
                            if cv2.waitKey(2) & 0xFF == ord('q'):
                                break
        
    except KeyboardInterrupt:
        Stop(motor1,motor2,motor3,motor4)
        
    except:
        print('Unknown Error Occured')
        
    finally:
        GPIO.cleanup()
        #current, peak = tracemalloc.get_traced_memory()
        #print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        #tracemalloc.stop()
        video.release()
        cv2.destroyAllWindows()
