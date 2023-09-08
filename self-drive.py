# -*- coding: utf-8 -*-
import cv2
import numpy as np
from openni import openni2
import math
import serial

x=range(0,255)
h=list()

for i in x:
    h.append(i)

font = cv2.FONT_HERSHEY_SIMPLEX

def oghlidosi_distance(x,y):
    return (math.sqrt(math.pow((x[0]-x[1]),2.0)+math.pow((y[0]-y[1]),2.0)))
    

openni2.initialize()     # can also accept the path of the OpenNI redistribution

dev = openni2.Device.open_any()

depth_stream = dev.create_depth_stream()
rgb_stream = dev.create_color_stream()
depth_stream.start()
rgb_stream.start()

lower = np.array([108,143,142])
upper = np.array([141, 255,255])



ser = serial.Serial("COM11", 9600,timeout=.1)

while True:


    frame = depth_stream.read_frame()
    
    frame_data = frame.get_buffer_as_uint16()
    depth = np.array(frame_data)
    #img = np.frombuffer(frame_data, dtype=np.uint16)

    depth = np.reshape(depth, [frame.height, frame.width])
    rgb = rgb_stream.read_frame()
    rgb = np.array(rgb.get_buffer_as_uint8())
    rgb = np.reshape(rgb, [frame.height, frame.width, 3])
    r=rgb[:,:,0]
    g=rgb[:,:,1]
    b=rgb[:,:,2]
    rgb[:,:,0]=r
    rgb[:,:,1]=g
    rgb[:,:,2]=b
    
    #img = np.concatenate((img, img, img), axis=0)

    #img = np.swapaxes(img, 0, 2)
    
    #img = np.swapaxes(img, 0, 1)
    
    
    if frame is None:
        break
    hsv_img = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV) 
    thresh_color = cv2.inRange(hsv_img, lower, upper)
    erodeimage=cv2.dilate(thresh_color,None,1)
    erodeimage=cv2.dilate(thresh_color,None,1)
    erodeimage=cv2.dilate(thresh_color,None,1)
    erodeimage=cv2.dilate(thresh_color,None,1)


    _,cnts,_= cv2.findContours(erodeimage, cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts)>=2 :
         max_contour = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
         max_contour2 = sorted(cnts, key=cv2.contourArea, reverse=True)[1]
         
         cnt1=cv2.contourArea(max_contour)
         cnt2=cv2.contourArea(max_contour2)
         deltacnt=cnt1-cnt2
         p = cv2.arcLength(max_contour ,True)
         p2 = cv2.arcLength(max_contour2 ,True)
         (x,y),r =cv2.minEnclosingCircle(max_contour)
         (x2,y2),r2 =cv2.minEnclosingCircle(max_contour2)

         center= (int(x),int(y))
         depthcenter=(depth[center[1],center[0]])/1000
         center2= (int(x2),int(y2))
         depthcenter2=(depth[center2[1],center2[0]])/1000
         radious =int(r)
         radious2 =int(r2)
         if center[0]>center2[0]:
             r2=oghlidosi_distance(center,(230, 639))
             r1=oghlidosi_distance(center2,(230, 639))
         else:
             r2=oghlidosi_distance(center2,(230, 639))
             r1=oghlidosi_distance(center,(230, 639))
         
         f=depthcenter-depthcenter2
         deltar=r1-r2
         diff=center[1]-center2[1]
         teta=(((diff/3)+6.16))


         diff=center[1]-center2[1]
         rect =cv2.minAreaRect(max_contour)
         rect2 =cv2.minAreaRect(max_contour2)

         box =cv2.boxPoints(rect)
         box2 =cv2.boxPoints(rect2)
         box =box.astype(int)
         box2 =box2.astype(int)
         cv2.drawContours(rgb, [box], -1, (0 ,255 ,0), 3)
         cv2.drawContours(rgb, [box2], -1, (0 ,255 ,0), 3)
         cv2.line(rgb, (320, 480), center, (255, 255, 255), 3)
         cv2.line(rgb, (320, 480), center2, (255, 255, 255), 3)
         cv2.putText(rgb ,"r1: {}".format(r1) ,(30,20),font,0.9 ,(0,255,0),2)
         cv2.putText(rgb ,"r2: {}".format(r2) ,(30,40),font,0.9 ,(255,0,0),2)
         cv2.putText(rgb ,"deltar: {}".format(deltar) ,(30,60),font,0.9 ,(0,0,255),2)
         cv2.putText(rgb ,"deltacnt: {}".format(deltacnt) ,(30,80),font,0.9 ,(0,0,255),2)
         cv2.putText(rgb ,"teta: {}".format(teta) ,(30,100),font,0.9 ,(0,0,255),2)
         print("deltacnt")
         print(deltacnt)
         if r2>r1 :
            k=1
         if r2<=r1:
            k=-1
        
   
         if diff!=0 :
             if diff<2 and diff>=-2 :
                ser.write(bytes([2]))
           
             else:
                teta=1*(((diff/3)+6.16))
                print("teta:")
                print(teta)
                print("diff:")
                print(diff)
                #ser.write(str(teta).encode("UTF-8"))
                if k==-1 :
                    k=2
                if k==1 :
                    k=1
                ser.write(bytes([k]))
                if int(teta)<254 :
                  f=int(teta)
                  ser.write(bytes([abs(f)])) 
                    
            
            
                print("0000000")
                RawData=ser.readline()
                print("reasived data:")
                print(RawData)
                print("0000000")
 
#cv2.drawContours(image1,cnts, -1, (0 ,255 ,0), 2)
#x,y,w,h =cv2.boundingRect(cnts)
#cv2.rectangle(and_img , (x,y),(x+w,y+h),(0,255,0),-1)
                
    cv2.imshow("test", rgb)
    if cv2.waitKey(30)== ord('q'):
        break
cv2.waitKey(0)
cv2.destroyAllWindows()
ser.close()
