# -*- coding: utf-8 -*-
import cv2
import numpy as np
from openni import openni2
import math
import serial

# Define the range of colors to detect
lower = np.array([108,143,142])
upper = np.array([141, 255,255])

# Initialize the OpenNI library
openni2.initialize()

# Open any available device
dev = openni2.Device.open_any()

# Create depth and RGB streams
depth_stream = dev.create_depth_stream()
rgb_stream = dev.create_color_stream()

# Start the streams
depth_stream.start()
rgb_stream.start()

# Create a font for displaying text on the image
font = cv2.FONT_HERSHEY_SIMPLEX

# Function to calculate the Euclidean distance between two points
def oghlidosi_distance(x, y):
    return math.sqrt(math.pow((x[0]-x[1]), 2.0) + math.pow((y[0]-y[1]), 2.0))

# Connect to the serial port
ser = serial.Serial("COM11", 9600, timeout=.1)

while True:
    # Read a frame from the depth stream
    frame = depth_stream.read_frame()
    
    # Get the depth data from the frame
    frame_data = frame.get_buffer_as_uint16()
    depth = np.array(frame_data)
    depth = np.reshape(depth, [frame.height, frame.width])
    
    # Read a frame from the RGB stream
    rgb = rgb_stream.read_frame()
    rgb = np.array(rgb.get_buffer_as_uint8())
    rgb = np.reshape(rgb, [frame.height, frame.width, 3])
    
    # Convert the RGB image to HSV color space
    hsv_img = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV) 
    
    # Threshold the image to detect the specified color range
    thresh_color = cv2.inRange(hsv_img, lower, upper)
    
    # Perform morphological operations to remove noise
    erodeimage = cv2.dilate(thresh_color, None, 1)
    erodeimage = cv2.dilate(thresh_color, None, 1)
    erodeimage = cv2.dilate(thresh_color, None, 1)
    erodeimage = cv2.dilate(thresh_color, None, 1)

    # Find contours in the thresholded image
    _, cnts, _ = cv2.findContours(erodeimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If at least two contours are found
    if len(cnts) >= 2:
        # Sort the contours by area in descending order
        max_contour = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        max_contour2 = sorted(cnts, key=cv2.contourArea, reverse=True)[1]
        
        # Calculate the areas of the contours
        cnt1 = cv2.contourArea(max_contour)
        cnt2 = cv2.contourArea(max_contour2)
        
        # Calculate the difference in areas
        deltacnt = cnt1 - cnt2
        
        # Calculate the perimeter of the contours
        p = cv2.arcLength(max_contour, True)
        p2 = cv2.arcLength(max_contour2, True)
        
        # Calculate the minimum enclosing circle for each contour
        (x, y), r = cv2.minEnclosingCircle(max_contour)
        (x2, y2), r2 = cv2.minEnclosingCircle(max_contour2)

        # Calculate the center coordinates and depth values for each contour
        center = (int(x), int(y))
        depthcenter = depth[center[1], center[0]] / 1000
        center2 = (int(x2), int(y2))
        depthcenter2 = depth[center2[1], center2[0]] / 1000
        
        # Calculate the radii of the circles
        radious = int(r)
        radious2 = int(r2)
        
        # Determine the orientation of the circles based on their x-coordinates
        if center[0] > center2[0]:
            r2 = oghlidosi_distance(center, (230, 639))
            r1 = oghlidosi_distance(center2, (230, 639))
        else:
            r2 = oghlidosi_distance(center2, (230, 639))
            r1 = oghlidosi_distance(center, (230, 639))
        
        # Calculate the difference in radii and y-coordinates
        deltar = r1 - r2
        diff = center[1] - center2[1]
        
        # Calculate the angle of rotation
        teta = (((diff / 3) + 6.16))
        
        # Draw the contours, circles, and lines on the RGB image
        rect = cv2.minAreaRect(max_contour)
        rect2 = cv2.minAreaRect(max_contour2)
        box = cv2.boxPoints(rect)
        box2 = cv2.boxPoints(rect2)
        box = box.astype(int)
        box2 = box2.astype(int)
        cv2.drawContours(rgb, [box], -1, (0, 255, 0), 3)
        cv2.drawContours(rgb, [box2], -1, (0, 255, 0), 3)
        cv2.line(rgb, (320, 480), center, (255, 255, 255), 3)
        cv2.line(rgb, (320, 480), center2, (255, 255, 255), 3)
        
        # Display the radii and differences on the image
        cv2.putText(rgb, "r1: {}".format(r1), (30, 20), font, 0.9, (0, 255, 0), 2)
        cv2.putText(rgb, "r2: {}".format(r2), (30, 40), font, 0.9, (255, 0, 0), 2)
        cv2.putText(rgb, "deltar: {}".format(deltar), (30, 60), font, 0.9, (0, 0, 255), 2)
        cv2.putText(rgb, "deltacnt: {}".format(deltacnt), (30, 80), font, 0.9, (0, 0, 255), 2)
        cv2.putText(rgb, "teta: {}".format(teta), (30, 100), font, 0.9, (0, 0, 255), 2)
        
        # Print the deltacnt value
        print("deltacnt")
        print(deltacnt)
        
        # Determine the value of k based on the radii
        if r2 > r1:
            k = 1
        if r2 <= r1:
            k = -1
        
        # If the difference in y-coordinates is not zero
        if diff != 0:
            # If the difference is small, send a command to the serial port
            if diff < 2 and diff >= -2:
                ser.write(bytes([2]))
            else:
                # Calculate the angle of rotation and send commands to the serial port
                teta = 1 * (((diff / 3) + 6.16))
                print("teta:")
                print(teta)
                print("diff:")
                print(diff)
                if k == -1:
                    k = 2
                if k == 1:
                    k = 1
                ser.write(bytes([k]))
                if int(teta) < 254:
                    f = int(teta)
                    ser.write(bytes([abs(f)])) 
                
                print("0000000")
                RawData = ser.readline()
                print("reasived data:")
                print(RawData)
                print("0000000")
 
    # Display the RGB image
    cv2.imshow("test", rgb)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(30) == ord('q'):
        break

# Release resources
cv2.waitKey(0)
cv2.destroyAllWindows()
ser.close()

