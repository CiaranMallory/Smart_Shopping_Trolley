 
import cv2
import matplotlib.pyplot as plt
import math
import numpy as np
from centroidtracker import CentroidTracker
import tracemalloc

#tracemalloc.start()

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

# Function used to process video feed and send movement commands to pi
def Movement(center, objectId):
    if(objectId == 0):
        if(center[0] < 130):
            print('Left')
        if(center[0] > 230):
            print('Right')
        else:
            print("No movement")
        #if(center[1] > 1200):
        #    print('Forward')
        #if(center[1] < 720):
        #    print('Stop')

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

# Run continuously
while True:
    # Configure frame
    ret, frame = video.read()
    #cv2.line(frame, pt1=(330,0), pt2=(330,600), color=(0,0,255), thickness=5)
    #cv2.line(frame, pt1=(140,0), pt2=(140,600), color=(0,0,255), thickness=5)
    #height, width, _ = frame.shape
    #print(height, width)

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
                Movement(center, objectId)

    # Display video
    cv2.imshow('Object Detection',frame)
    
    # Cancel video playback if 'q' key is pressed
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break


#current, peak = tracemalloc.get_traced_memory()
#print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
#tracemalloc.stop()
video.release()
cv2.destroyAllWindows()