from cv2.cv import *
import cv2
import numpy
import sys
from time import sleep

capture = CaptureFromCAM(0)  # 0 -> index of camera
if capture:     # Camera initialized without any errors
   NamedWindow("cam-test",CV_WINDOW_AUTOSIZE)
   for x in xrange(10):
       f = QueryFrame(capture)     # capture the frame
       arr = numpy.asarray(f[:,:], dtype=numpy.uint8)
       arr = arr[:,120:520]
       im = cv2.resize(arr, (92, 112)) 
       gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
       cv2.imwrite('samples/'+str(x+1)+'.pgm', gray)
       sleep(0.5)
   if f:
       ShowImage("cam-test",fromarray(gray))
       WaitKey(0)
DestroyWindow("cam-test")
