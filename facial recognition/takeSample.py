from cv2.cv import *
import cv2
import numpy
import sys
from time import sleep

capture = CaptureFromCAM(0)  # 0 -> index of camera
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
if capture:     # Camera initialized without any errors
   NamedWindow("cam-test",CV_WINDOW_AUTOSIZE)
   count = 0;
   while count < 10:
      f = QueryFrame(capture)     # capture the frame
      arr = numpy.asarray(f[:,:], dtype=numpy.uint8)
      gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(
         gray,
         scaleFactor=1.1,
         minNeighbors=5,
         minSize=(30, 30),
         flags = cv2.cv.CV_HAAR_SCALE_IMAGE
      )
      if len(faces) != 0:
         (x,y,w,h) = faces[0]
         d = w * 112 / 184
         print d
         im = gray[(y-0.5*d):(y+1.5 * d), x:(x+w)]
         im = cv2.resize(im, (92, 112)) 
         cv2.imwrite('samples/'+str(count+1)+'.pgm', im)
         count = count +1
      sleep(0.5)
   if f:
      ShowImage("cam-test",fromarray(im))
      WaitKey(0)
DestroyWindow("cam-test")
