# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 18:57:33 2018

@author: vi1877
"""

import numpy as np
import cv2 as cv

img = cv.imread('train-ticket.png')
b,g,r =  cv.split(img)

mask = np.where(r > 150)
b[mask] = 255
g[mask] =255
r.max()

img2 = cv.merge([b,g,r])
img_grey = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
img_threshd = cv.threshold(img_grey, 230, 230, cv.THRESH_BINARY)
