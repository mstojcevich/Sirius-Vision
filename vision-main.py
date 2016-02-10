from SimpleCV import *
import numpy as np
import time
import math
from PyQt4 import *

minHue = 74
maxHue = 103

minLum = 46
maxLum = 120

minSat = 183
maxSat = 255

camNum = 0  # Camera number from the OS. Usually starts at 0.
cam = SimpleCV.Camera(camNum)

while True:
    img = cam.getImage().toHLS()  # Grab image from cam, convert to (hue, luminosity, saturation)
    segmented = Image(cv2.inRange(img.rotate90().getNumpyCv2(),  # filter the image based on HSV ranges
                                  np.array([minHue, minLum, minSat]),
                                  np.array([maxHue, maxLum, maxSat])))
    
    blobs = segmented.findBlobs() # Find blobs
    
    # Draw blobs if their radius > 20
    if blobs:
        for b in blobs:
            if b.radius() > 20:
                b.drawHull(color=(0, 128, 0), alpha=-1, width=-1, layer=None)  # Draw hull around blob
                
                # Draw an estimated rectangle bound for the blob
                rect_width = b.width()
                rect_height = b.height()
                rect_ctr_x = b.minRectX()
                mrX = rect_ctr_x - rect_width / 2
                mrY = b.minRectY() - rect_height / 2
                segmented.drawRectangle(mrX, mrY, rect_width,
                                        rect_height, color=Color.ORANGE, width=6)
    
    segmented.show()  # Displays the filtered and segmented image on the screen in a window
