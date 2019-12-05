import numpy as np
import cv2
from Utilities import *
from math import ceil, floor

def getHistogram(Img, angle = 0, bins = 8):
    Histogram = np.zeros(bins)

    # (h, w) = Img.shape[:2]

    # # showImage(Img, '1')
    # # Square the image
    # MaxD = int(max(h, w))
    # WPadding = (MaxD - w) / 2
    # HPadding = (MaxD - h) / 2
    # Img = cv2.copyMakeBorder(Img, ceil(HPadding), floor(HPadding), ceil(WPadding), floor(WPadding), cv2.BORDER_CONSTANT, value = (0, 0, 0))
    # (h, w) = Img.shape[:2]

    # # showImage(Img, '2')

    # Size = (200, 200)
    # Img = cv2.resize(Img, Size)
    # (h, w) = Img.shape[:2]
    
    # # showImage(Img, '3')

    # Padding = 100
    # Img = cv2.copyMakeBorder(Img, Padding, Padding, Padding, Padding, cv2.BORDER_CONSTANT, value = (0, 0, 0))
    # (h, w) = Img.shape[:2]

    # # showImage(Img, '4')

    # center = (w // 2, h // 2)
    # M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Img = cv2.warpAffine(Img, M, (h, w), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # (h, w) = Img.shape[:2]

    (h, w) = Img.shape

    Img = safetyPadding(Img)

    Img = rotateImage(Img, angle)

    Img = blackAndWhite(Img)

    SlotWidth = ceil(h / bins)
    # showImage(Img, '5')
    for _bin in range(bins):
        Slice = Img[_bin * SlotWidth: (_bin + 1) * SlotWidth, :]
        # showImageZoomed(Slice)
        Histogram[_bin] += len(np.where(Slice == 255)[0])

    return Histogram

def getHistogramH(img, bins = 8):
    Histogram = np.zeros(bins)
    
    (h, w) = img.shape

    SlotWidth = ceil(h / bins)
    # showImage(Img, '5')
    for _bin in range(bins):
        Slice = img[_bin * SlotWidth: (_bin + 1) * SlotWidth, :]
        Histogram[_bin] += len(np.where(Slice == 255)[0])
    # print(Histogram)
    return Histogram

def getHistogramV(img, bins = 8):
    Histogram = np.zeros(bins)
    
    (h, w) = img.shape

    SlotWidth = ceil(w / bins)
    # showImage(Img, '5')
    for _bin in range(bins):
        Slice = img[:, _bin * SlotWidth: (_bin + 1) * SlotWidth]
        Histogram[_bin] += len(np.where(Slice == 255)[0])
    # print(Histogram)
    return Histogram

# Riad
# def Algo1(img):
#     for Y, Row in enumerate(img):
#         for X, Pixel in enumerate(Row):
            