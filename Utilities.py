import cv2
import numpy as np
from math import ceil, floor, sqrt
import copy

# Cigirates after sex

def showImage(img, name = "image", waitkey = True, points = None):
    showImageZoomed(img, ratio=1, name = name, points = points, waitkey = waitkey, seperate = 0)

def closeAllWindows(waitkey = True):
    if waitkey:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cv2.destroyAllWindows()

def showImageZoomed(img, ratio = 15, name = "image", points=None, waitkey = True, seperate = 1):
    size = ((img.shape[0] * (ratio + seperate)), (img.shape[1] * (ratio + seperate)))
    if points != None:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img[img > 0] = 255
        for point in points:
            img[point[0], point[1], 0] = img[point[0], point[1], 0] - 150
            img[point[0], point[1], 1] = img[point[0], point[1], 1] - 150
        zoomed = np.zeros((size[0], size[1], 3), np.uint8)
    else:
        if len(img.shape) == 3:
            zoomed = np.zeros((size[0], size[1], 3), np.uint8)
        else:
            zoomed = np.zeros(size)
    for Y, Row in enumerate(img):
        for X, Pixel in enumerate(Row):
            zoomed[Y*ratio + seperate * Y: (Y + 1)*ratio + seperate * Y, X*ratio + seperate * X: (X + 1)*ratio + seperate * X] = Pixel

    cv2.imshow(name,zoomed)
    if waitkey:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def showMultipleImages(imgs, ratio = 15, name = "image", points=None, waitkey = True, seperate = 1):
    size = imgs[0].shape
    # [print(img.shape) for img in imgs]
    assert all(img.shape[0] == size[0] and img.shape[1] == size[1] for img in imgs)
    assert all(len(img.shape) != 3 for img in imgs)

    # Values = [Chr for Chr in '0123456789ABCDEF']
    Colors = []
    while len(Colors) != len(imgs):
        Color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        if Color[0] + Color[1] + Color[2] > 255 * 2:
            Colors.append(Color)
    # print(Colors)

    size = ((size[0] * (ratio + seperate)), (size[1] * (ratio + seperate)))
    
    zoomed = np.zeros((size[0], size[1], 3), np.uint8)

    for idx, img in enumerate(imgs):
        Color = Colors[idx]
        for Y, Row in enumerate(img):
            for X, Pixel in enumerate(Row):
                if Pixel != 0:
                    Pixel = Pixel / 255
                    PixelValue = (int(Color[0] * Pixel), int(Color[1] * Pixel), int(Color[2] * Pixel))
                    zoomed[Y*ratio + seperate * Y: (Y + 1)*ratio + seperate * Y, X*ratio + seperate * X: (X + 1)*ratio + seperate * X] = PixelValue

    if points is not None:
        for point in points:
            Y = point[0]
            X = point[1]
            PixelValue = 150
            zoomed[Y*ratio + seperate * Y: (Y + 1)*ratio + seperate * Y, X*ratio + seperate * X: (X + 1)*ratio + seperate * X, 0:2] = PixelValue

    cv2.imshow(name,zoomed)
    if waitkey:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def loadImage(img_path, grayscale = True):
    if grayscale:
        return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) 
    else: 
        return cv2.imread(img_path)

def invertImage(img):
    return 255 - img[:, :]

def blackAndWhite(img, thrs = 100):
    img = img.copy()
    img[img > thrs] = 255
    img[img <= thrs] = 0
    return img
    
def removePadding(img, padding = None, thrs = 200):
    if padding is None:
        WhitePixels = np.where(img > 200)
        MinY = min(WhitePixels[0])
        MaxY = max(WhitePixels[0])
        MinX = min(WhitePixels[1])
        MaxX = max(WhitePixels[1])
        return img[MinY: MaxY + 1, MinX: MaxX + 1]
    else:
        h, w = img.shape
        hpadding = padding[0]
        wpadding = padding[1]
        return img[hpadding: h - 2 * hpadding + 1, wpadding: w - 2 * wpadding + 1]
        
def getPixel(point, img):
    size = img.shape
    if -1 < point[0] < size[0] and -1 < point[1] < size[1]:
        return img[point[0], point[1]], True
    else:
        return 0, False
 
def rotateImage(img, angle = 0):

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return img

def safetyPadding(img):
    
    h, w = img.shape
    Padding = ceil(sqrt(h**2 + w**2))
    HPadding, WPadding = Padding - h, Padding - w
    img = cv2.copyMakeBorder(img, HPadding, HPadding, WPadding, WPadding, cv2.BORDER_CONSTANT, value = (0, 0, 0))

    return img, HPadding, WPadding

def addPadding(img, hpadding, wpadding):
    
    img = cv2.copyMakeBorder(img, hpadding, hpadding, wpadding, wpadding, cv2.BORDER_CONSTANT, value = (0, 0, 0))

    return img

def elementwiseAdding(a, b):
    assert len(a) == len(b)
    Result = (a[Index] + b[Index] for Index in range(len(a)))
    return tuple(Result)

# def zhangSuen(img):
#     # P9  	  P2  	  P3  
#     # P8  	  P1  	  P4  
#     # P7  	  P6  	  P5  

#     img[img > 100] = 255
#     img[img <= 100] = 0

#     def getAdjs(img, point):
#         Y, X = point
#         EightAdjs = True
#         P2, C = getPixel((Y - 1, X), img)
#         EightAdjs = EightAdjs and C
#         P3, C = getPixel((Y - 1, X + 1), img)
#         EightAdjs = EightAdjs and C
#         P4, C = getPixel((Y, X + 1), img)
#         EightAdjs = EightAdjs and C
#         P5, C = getPixel((Y + 1, X + 1), img)
#         EightAdjs = EightAdjs and C
#         P6, C = getPixel((Y + 1, X), img)
#         EightAdjs = EightAdjs and C
#         P7, C = getPixel((Y + 1, X - 1), img)
#         EightAdjs = EightAdjs and C
#         P8, C = getPixel((Y, X - 1), img)
#         EightAdjs = EightAdjs and C
#         P9, C = getPixel((Y - 1, X - 1), img)
#         EightAdjs = EightAdjs and C
#         return P2, P3, P4, P5, P6, P7, P8, P9, EightAdjs

#     def getTransitions(img, point, adjs):
#         Transitions = 0
#         CurrentValue = Adjs[-1]
#         for Index in range(len(adjs)):
#             if adjs[Index] != CurrentValue and CurrentValue == 0:
#                 Transitions += 1
#             CurrentValue = adjs[Index]

#         return Transitions

#     def getWhites(img, point, adjs):
#         return len(np.where(adjs == 255)[0])

#     Done = False
#     while not Done:
#         Done = True
#         ToErase = []
#         for Y, Row in enumerate(img):
#             for X, Pixel in enumerate(Row):
#                 if Pixel != 255:
#                     continue

#                 P2, P3, P4, P5, P6, P7, P8, P9, EightAdjs = getAdjs(img, (Y, X))
#                 Adjs = [P2, P3, P4, P5, P6, P7, P8, P9]
#                 if EightAdjs and 2 <= getWhites(img, (Y, X), Adjs) <= 6 and getTransitions(img, (Y, X), Adjs) == 1 and (P2 == 0 or P4 == 0 or P6 == 0) and (P4 == 0 or P6 == 0 or P8 == 0):
#                     ToErase.append((Y, X))
#                     Done = False

#         # for Y, X in ToErase:
#         #     img[Y, X] = 0
#         # ToErase = []
#         for Y, Row in enumerate(img):
#             for X, Pixel in enumerate(Row):
#                 if Pixel != 255:
#                     continue

#                 P2, P3, P4, P5, P6, P7, P8, P9, EightAdjs = getAdjs(img, (Y, X))
#                 Adjs = [P2, P3, P4, P5, P6, P7, P8, P9]
#                 if EightAdjs and 2 <= getWhites(img, (Y, X), Adjs) <= 6 and getTransitions(img, (Y, X), Adjs) == 1 and (P2 == 0 or P4 == 0 or P8 == 0) and (P2 == 0 or P6 == 0 or P8 == 0):
#                     ToErase.append((Y, X))
#                     Done = False

#         for Y, X in ToErase:
#             img[Y, X] = 0

#     return img


# img = loadImage('1.png')
# showImageZoomed(img, ratio= 10)
# showImageZoomed(zhangSuen(img), ratio= 10)
