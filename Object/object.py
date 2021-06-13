import numpy as np
import argparse
import cv2
import sys
#construct the argument parse and parse the arguments
fp=0.6
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", default='img.jpg' ,
     help="path to input image")
ap.add_argument("-p", "--prototxt", default='deploy.prototxt',
     help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model",default='MobileNetSSD_deploy.caffemodel',
     help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
     help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
     "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
     "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
     "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
print("[INFO] loading model…")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
image = cv2.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
print("[INFO] computing object detections…")
net.setInput(blob)
detections = net.forward()
for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
                idx = int(detections[0, 0, i, 1])
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                lab=CLASSES[idx]
                print("[INFO] {}".format(label))
                if confidence > fp:
                        save = open('frame.txt', "a+")
                        print(lab,file=save)
                        save.close()

		

