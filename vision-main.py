from SimpleCV import *
import numpy as np
import time
import math
from PyQt4 import *

minHue = 74
minSat = 183
minLum = 46
maxHue = 103
maxSat = 255
maxLum = 120
camNum = 0
cam = SimpleCV.Camera(camNum)

while True:
    img = cam.getImage().toHLS()  # Grabbing image and converting it to SimpleCV Hue Luminance and Saturation value
    segmented = Image(cv2.inRange(img.rotate90().getNumpyCv2(),  # filters the image based on given values
                                  np.array([minHue, minLum, minSat]),
                                  np.array([maxHue, maxLum, maxSat])))
    ''' -----------code to convert image to cv2 image, may need to use for further use of this program----------------
        cv_segmented = segmented.getNumpy()
        greySegmented = cv2.cvtColor(cv_segmented, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(greySegmented, 127, 255, 0)
        im2, contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    '''
    blobs = segmented.findBlobs()
    # Look for and draw blobs if they are above radius 20
    if blobs:
        for b in blobs:
            if b.radius() > 20:
                b.drawHull(color=(0, 128, 0), alpha=-1, width=-1, layer=None)  # Draws blob
                # lines 32-38 are getting rectangle points and drawing a bounding rectangle around the blobs
                rect_width = b.width()
                rect_height = b.height()
                rect_ctr_x = b.minRectX()
                mrX = rect_ctr_x - rect_width / 2
                mrY = b.minRectY() - rect_height / 2
                segmented.drawRectangle(mrX, mrY, rect_width,
                                        rect_height, color=Color.ORANGE, width=6)
    segmented.show()  # Displays the filtered/segmented image on the screen in a window
