# import the necessary packages
import numpy as np
import argparse
import time
import os
import cv2
from count import count
from gtts import gTTS
import audioread
import vlc

file1="result.mp3"
file2="result1.txt"
file3="result.txt"
if os.path.exists(file1)==True:
    os.remove(file1)
if os.path.exists(file2)==True:
    os.remove(file2)
if os.path.exists(file3)==True:
    os.remove(file3)

def capture():
    cam = cv2.VideoCapture(0)
    ret,img=cam.read()
    cv2.imwrite("img.jpg",img)

def object_det():
#     say=gTTS("Recognising....")
#     say.save("play.mp3")
#     with audioread.audio_open('play.mp3') as f:
#         totalsec = f.duration
#         
#     p=vlc.MediaPlayer("play.mp3")
#     p.play()
#     time.sleep(totalsec)
    
    cam = cv2.VideoCapture(0)
    ret,img=cam.read()
    cv2.imwrite("img.jpg",img)
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', default="img.jpg", help='path to the input image')
    # ap.add_argument('-p', '--prototxt', default='/Users/siddhantbansal/Desktop/Python/Personal_Projects/Object_Detection/MobileNetSSD_deploy.prototxt.txt', help='path to Caffe deploy prototxt file')
    # ap.add_argument('-m', '--model', default='/Users/siddhantbansal/Desktop/Python/Personal_Projects/Object_Detection/MobileNetSSD_deploy.caffemodel', help='path to the Caffe pre-trained model')
    ap.add_argument('-p', '--prototxt', default="MobileNetSSD_deploy.prototxt.txt", help='path to Caffe deploy prototxt file')
    ap.add_argument('-m', '--model', default="MobileNetSSD_deploy.caffemodel", help='path to the Caffe pre-trained model')
    ap.add_argument('-c', '--confidence', type=float, default=0.7, help='minimum probability to filter weak detections')
    args = vars(ap.parse_args())

    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    #print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    # (note: normalization is done via the authors of the MobileNet SSD
    # implementation)
    image = cv2.imread(args['image'])
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the neural network
    #print('[INFO] computing object detection...')
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., the probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the 'confidence' is greater than the minimum confidence
        if confidence > args['confidence']:
            # extract the index of the classes label from the 'detections',
            # then compute the (x, y)-coordinates of the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype('int')

            # display the prediction
            label = "{}".format(CLASSES[idx], confidence * 100)
            #print("{}\n".format(label))
            text = "".join([c if ord(c) < 128 else "" for c in label]).strip()
            save = open("result1.txt", "a+")
            print (text,file=save)
            save.close()
            
            cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # show the output image
    #cv2.imshow('Output', image)
    cv2.waitKey(0)


capture()
object_det()
count(file2)
if os.path.exists(file3)==True:
    f= open("result.txt", "r")
    text = f.read()
    f.close()
    tts = gTTS(text)
    tts.save("result.mp3")

    with audioread.audio_open('result.mp3') as f:
        totalsec = f.duration
        
    p=vlc.MediaPlayer("result.mp3")
    p.play()
    time.sleep(totalsec)
    
else:
    tts=gTTS("Recognision Failed Please Try Again")
    tts.save("result.mp3")
    with audioread.audio_open('result.mp3') as f:
        totalsec = f.duration
        
    p=vlc.MediaPlayer("result.mp3")
    p.play()
    time.sleep(totalsec)

