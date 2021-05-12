from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys
import numpy as np
import cv2

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

class InfraRedRuntime(object):
    def __init__(self):
        # pygame.init()

        # Used to manage how fast the screen updates
        # self._clock = pygame.time.Clock()

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared)

        # back buffer surface for getting Kinect infrared frames, 8bit grey, width and height equal to the Kinect color frame size
        # self._frame_surface = pygame.Surface((self._kinect.infrared_frame_desc.Width, self._kinect.infrared_frame_desc.Height), 0, 24)
        # here we will store skeleton data 
        # self._bodies = None
        
        # Set the width and height of the screen [width, height]
        # self._infoObject = pygame.display.Info()
        # self._screen = pygame.display.set_mode((self._kinect.infrared_frame_desc.Width, self._kinect.infrared_frame_desc.Height), 
                                                # pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        # pygame.display.set_caption("Kinect for Windows v2 Infrared")

    def show_infrared_frame(self, frame):
        frame = np.float32(frame)
        Infrared_threshold = 65535
        scale = 2
        image_infrared_all = frame.reshape([self._kinect.depth_frame_desc.Height,
                                            self._kinect.depth_frame_desc.Width])
        # 转换为（n，m，1） 形式
        image_infrared_all = image_infrared_all * scale
        image_infrared_all[image_infrared_all > Infrared_threshold] = Infrared_threshold        
        image_infrared_all = image_infrared_all / Infrared_threshold * 255
        image_infrared_all = np.uint8(image_infrared_all)
        result = infrared = image_infrared_all[:,::-1]
        return result

    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            # for event in pygame.event.get(): # User did something
            #     if event.type == pygame.QUIT: # If user clicked close
            #         self._done = True # Flag that we are done so we exit this loop

            #     elif event.type == pygame.VIDEORESIZE: # window resized
            #         self._screen = pygame.display.set_mode(event.dict['size'], 
            #                                     pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    

            # --- Getting frames and drawing  
            if self._kinect.has_new_infrared_frame():
                frame = self._kinect.get_last_infrared_frame()
                ir_frame = self.show_infrared_frame(frame)
                cv2.imshow("ir", ir_frame)
                cv2.waitKey(1)
            
            # --- Limit to 60 frames per second
            self._clock.tick(60)
            
        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        # pygame.quit()


__main__ = "Kinect v2 InfraRed"
game =InfraRedRuntime();
game.run();


