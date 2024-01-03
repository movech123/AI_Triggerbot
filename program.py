from pynput.keyboard import Key, Controller 
import torch 
import numpy as np
import mss
from pynput import mouse
import pyautogui as pag 
import random 
import time 
import threading
import pygetwindow as gw  
from ultralytics import YOLO
import math
import cv2
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
board = Controller()


MONITOR_WIDTH = 1920#game res
MONITOR_HEIGHT = 1080#game res
MONITOR_SCALE = 5#how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions
region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
x,y,width,height = region
screenshot_center = [int((width-x)/2),int((height-y)/2)]

model = torch.hub.load('C:/Users/vmoda/OneDrive/Desktop/val/yolov5', 'custom', path= 'C:/Users/vmoda/OneDrive/Desktop/val/best.pt',source='local')
model.conf = 0.40
model.maxdet = 6
model.amp = True 
model.classes = [1]


start_time = time.time()
x = 1
counter = 0

closest_dist = 100000000000
closest = -1




with mss.mss() as stc:
    while True:
        closest_dist = 100000000000
        closest = -1    
        screenshot = np.array(stc.grab(region))
        
        df = model(screenshot, size=736).pandas().xyxy[0]
        
    
        counter+= 1
        if(time.time() - start_time) > x:
            fps = "fps:"+ str(int(counter/(time.time() - start_time)))
            print(fps)
            counter = 0
            start_time = time.time()



        for i in range(0,4):
            try:
                xmin = int(df.iloc[i,0])
                ymin = int(df.iloc[i,1])
                xmax = int(df.iloc[i,2])
                ymax = int(df.iloc[i,3])

                centerX = (xmax-xmin)/2+xmin
                centerY = (ymax-ymin)/2+ymin
                
                distance = math.dist([centerX,centerY], screenshot_center)
                
                
                if int(distance) < closest_dist:
                    closest_dist=distance
                    closest = i

            except:
                pass

        
        if closest != -1:
            xmin = df.iloc[closest,0]
            ymin = df.iloc[closest,1]
            xmax = df.iloc[closest,2]
            ymax = df.iloc[closest,3]
            if screenshot_center[0] in range(int(xmin),int(xmax)) and screenshot_center[1] in range(int(ymin),int(ymax)):
                board.press('h')
                
                board.release('h')  # h is binded to alt fire 
                time.sleep(.5)
        
