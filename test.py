
def skeletonizePart(img):
    # WhitePixels = np.where(img == 255)
    # CenterX = floor(sum(WhitePixels[1]) / len(WhitePixels[1]))
    # CenterY = floor(sum(WhitePixels[0]) / len(WhitePixels[0]))

    # print(img[CenterY, CenterX])

    img[img > 100] = 255
    img[img <= 100] = 0

    Size = img.shape
        
    def check(adjs):
        # for Index in range(1, len(adjs)):
        #     if adjs[Index] == adjs[Index - 1] == 255:
        #         return False
        # # print("fgv")
        # return True

        CurrentValue = adjs[-1]
        Transitions = 0
        for Index in range(len(adjs)):
            if adjs[Index] != CurrentValue:
                Transitions += 1
                CurrentValue = adjs[Index]
        if Transitions >= 4:
            return True
        else:
            return False

    Done = False
    while not Done:
        Copy = copy.copy(img)
        Done = True

        for Y, Row in enumerate(img):
            for X, Pixel in enumerate(Row):
                if Pixel != 255:
                    continue
                # showImageZoomed(Copy, ratio=10, point=(Y, X))
                if sum(Copy[Y,:]) < 300:
                    Copy[Y, X] = 255
                    continue
                
                # if sum(Copy[:, X]) < 300:
                #     Copy[Y, X] = 255
                #     continue

                OldAdjs = [ getPixel((Y + 1, X - 1), img) , getPixel((Y + 1, X), img) , getPixel((Y + 1, X + 1), img) , getPixel((Y, X + 1), img) , getPixel((Y - 1, X + 1), img) , getPixel((Y - 1, X), img) , getPixel((Y - 1, X - 1), img) , getPixel((Y, X - 1), img) ]
                Adjs = [ getPixel((Y + 1, X - 1), Copy) , getPixel((Y + 1, X), Copy) , getPixel((Y + 1, X + 1), Copy) , getPixel((Y, X + 1), Copy) , getPixel((Y - 1, X + 1), Copy) , getPixel((Y - 1, X), Copy) , getPixel((Y - 1, X - 1), Copy) , getPixel((Y, X - 1), Copy) ]

                if check(Adjs):
                    Copy[Y, X] = 255
                else:
                    Copy[Y, X] = min(OldAdjs)
                    Done = False
                    
        showImageZoomed(Copy, ratio=10)
        img = Copy
    return img
    
def skeletonizePartWithAngle(img, angle = 0):
    img[img > 100] = 255
    img[img <= 100] = 0
    h, w = img.shape
    
    img, HPadding, WPadding = safetyPadding(img)
    img = rotateImage(img, angle)

    Copy = np.zeros(img.shape, np.uint8)
    for Y, Row in enumerate(img):
        for X, Pixel in enumerate(Row):
            if Pixel != 255:
                continue
            # showImageZoomed(img, ratio=10, point=(Y, X))
            Count = 1
            Right = 1
            Left = 1
            while Right >= 0 and Left >= 0:
                Right -= 0 if getPixel((Y, X + Count), img) == 255 else 1
                Left -= 0 if getPixel((Y, X - Count), img) == 255 else 1
                Count += 1
            if abs(Right - Left) <= 1:
                Copy[Y, X] = 255
            else:
                Copy[Y, X] = 0
                    
    Copy = rotateImage(Copy, -angle)
    Copy = Copy[HPadding + 1: HPadding + h + 1, WPadding + 1: WPadding + w + 1]
    return Copy

def skeletonizePart2(img):
    
    img[img > 100] = 255
    img[img <= 100] = 0

    Copy = np.zeros(img.shape, np.uint8)
    for Y, Row in enumerate(img):
        for X, Pixel in enumerate(Row):
            if Pixel != 255:
                continue
            # showImageZoomed(img, ratio=10, point=(Y, X))
            Count = 1
            Right = 1
            Left = 1
            while Right >= 0 and Left >= 0:
                Right -= 0 if getPixel((Y, X + Count), img) == 255 else 1
                Left -= 0 if getPixel((Y, X - Count), img) == 255 else 1
                Count += 1
            if abs(Right - Left) <= 1:
                Copy[Y, X] = 255
            else:
                # Copy[Y, X] = 0
                Count = 1
                Bottom = 1
                Top = 1
                while Bottom >= 0 and Top >= 0:
                    Bottom -= 0 if getPixel((Y + Count, X), img) == 255 else 1
                    Top -= 0 if getPixel((Y - Count, X), img) == 255 else 1
                    Count += 1
                if abs(Bottom - Top) <= 1:
                    Copy[Y, X] = 255
                else:
                    Copy[Y, X] = 0
                    
    return Copy
                

# Img = loadImage('1.png')
# showImageZoomed(cv2.add(skeletonizePartWithAngle(Img, 0), skeletonizePartWithAngle(Img, 0)), ratio=10)
# Parts = seperateToParts(Img)
# [showImage(Part) for Part in Parts]
# [skeletonizePart(Part) for Part in Parts]

# Img = loadImage('2.png')
# Parts = seperateToParts(Img)
# [showImageZoomed(cv2.add(skeletonizePartWithAngle(Part, 0), skeletonizePartWithAngle(Part, 90)), ratio=10) for Part in Parts]

# Img = loadImage('3.png')
# Parts = seperateToParts(Img)
# [showImage(Part) for Part in Parts]
# [skeletonizePart(Part) for Part in Parts]


from thin import *
img = loadImage('test.png')
img = fixSkew(img)
img = invertImage(img)
img = blackAndWhite(img)
words = seperateWords(img)
nword = 28
nword = 4
showImageZoomed(words[nword])
parts = seperateToParts(words[nword])


npart = 1
npart = 0
showImageZoomed(parts[npart], waitkey = False, name='original')
print(parts[npart].shape)
part = addPadding(parts[npart], 1, 1)
part[part <= 100] = 0
part[part > 0] = 1
thin = zhangSuen(part)

thin[thin != 0] = 255
showImageZoomed(thin, waitkey = False, name='thin')
seperateLetters(thin)
closeAllWindows();