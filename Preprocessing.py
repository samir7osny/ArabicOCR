import cv2
import numpy as np
from FeaturesExtractor import *

def fixSkew(img, thrs = 200):
    coords = np.column_stack(np.where(img > thrs))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return img

def seperateWords(img, flag = 125):
    RIndecies = [Index for Index, Row in enumerate(img) if sum(Row) < len(Row) * 2]
    for Index in RIndecies:
        img[Index, :] = flag
        
    Images = []
    ImgStarted = -1
    ImgEnded = -1
    for RIndex in range(img.shape[0]):
        if len([False for Pixel in img[RIndex, :] if Pixel != flag]) > 0 and ImgStarted == -1 and ImgEnded == -1:
            ImgStarted = RIndex
        elif len([False for Pixel in img[RIndex, :] if Pixel != flag]) == 0 and ImgStarted != -1 and ImgEnded == -1:
            ImgEnded = RIndex
        if ImgStarted != -1 and ImgEnded != -1:
            Images.append(img[ImgStarted:ImgEnded, :])
            ImgStarted = -1
            ImgEnded = -1

    WordsImages = []
    for Img in Images:
        CIndecies = [Index for Index in range(Img.shape[1]) if sum(Img[:, Index]) < len(Img[:, Index]) * 10]
        for Index in CIndecies:
            Img[:, Index] = flag
        ImgStarted = -1
        ImgEnded = -1
        for CIndex in reversed(range(Img.shape[1])):
            if len([False for Pixel in Img[:, CIndex] if Pixel != flag]) > 0 and ImgStarted == -1 and ImgEnded == -1:
                ImgStarted = CIndex
            elif len([False for Pixel in Img[:, CIndex] if Pixel != flag]) == 0 and ImgStarted != -1 and ImgEnded == -1:
                ImgEnded = CIndex
            if ImgStarted != -1 and ImgEnded != -1:
                WordsImages.append(Img[:, ImgEnded + 1:ImgStarted + 1])
                ImgStarted = -1
                ImgEnded = -1

    return WordsImages

def seperateLetters(img):
    bins = img.shape[0]
    Histogram = getHistogramH(img, bins=bins)
    Maxima = np.where(Histogram == max(Histogram))[0][0]
    showImageZoomed(img, points=[(Maxima, X) for X in range(img.shape[1])], waitkey=False)

    print(Maxima)
    

