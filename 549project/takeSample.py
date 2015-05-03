from cv2.cv import *
import cv2
import numpy
import sys
import picamera
import os
from time import sleep

def takePhoto(pathname):
   directory = 'faces/'+ pathname
   if not os.path.exists(directory):
      os.makedirs(directory)
   capture = picamera.PiCamera()
   face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
   if capture:     # Camera initialized without any errors
      count = 0;
      while count < 10:
         capture.capture('temp.bmp')
         f = cv2.imread('temp.bmp')
         arr = numpy.asarray(f[:,:], dtype=numpy.uint8)
         gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
         faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,
         minNeighbors=5,minSize=(30, 30),flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
         if len(faces) != 0:
            (x,y,w,h) = faces[0]
            d = w * 112 / 184
            print d
            im = gray[(y-0.5*d):(y+1.5 * d), x:(x+w)]
            im = cv2.resize(im, (92, 112)) 
            cv2.imwrite('faces/'+pathname+'/'+str(count+1)+'.pgm', im)
            count = count +1
