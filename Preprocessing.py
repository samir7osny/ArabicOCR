import cv2
import numpy as np
from FeaturesExtractor import *
from Thining import *

def fixSkew(img, thrs = 100):
    coords = np.column_stack(np.where(img > thrs))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    print(angle)
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return img

def fixSkewAngle(img):
    coords = np.column_stack(np.where(img == 255))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    return angle

def rotateImage(img, angle):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return img

def seperateLines(img):
    Histogram = getHistogramH(img, bins=img.shape[0])

    Maximums = list(np.where(Histogram > 0)[0])
    Maximums.append((img.shape[0] + 50)) # to append last interval

    StartInterval = -1
    EndInterval = -1
    LocalMaximums = []
    for Maximum in Maximums:
        if StartInterval == -1:
            StartInterval = Maximum
            EndInterval = Maximum
        elif Maximum - EndInterval < 3:
            EndInterval = Maximum
        else:
            HistogramInterval = Histogram[StartInterval: EndInterval + 1]
            MaxInterval = np.where(Histogram == max(HistogramInterval))
            MaxInterval = [Index for Index in MaxInterval[0] if StartInterval <= Index <= EndInterval][0]
            LocalMaximums.append(MaxInterval)
            StartInterval = -1
            EndInterval = -1

    Seperators = []
    for Idx in range(1, len(LocalMaximums)):
        MidPoint = (LocalMaximums[Idx] + LocalMaximums[Idx - 1]) // 2
        if Histogram[MidPoint] != 0:
            dIdx = 1
            Found = False
            while MidPoint - dIdx > LocalMaximums[Idx - 1] and MidPoint + dIdx < LocalMaximums[Idx]:
                if Histogram[MidPoint - dIdx] == 0:
                    Seperators.append(MidPoint - dIdx)
                    Found = True
                    break
                if Histogram[MidPoint + dIdx] == 0:
                    Seperators.append(MidPoint + dIdx)
                    Found = True
                    break
                dIdx += 1
            assert Found
        else:
            Seperators.append(MidPoint)

    Seperators = [0] + Seperators + [img.shape[0] - 1]
    return [img[Seperators[Idx]: Seperators[Idx + 1], :] for Idx in range(len(Seperators) - 1)]

def getBaseLine(line):
    Histogram = getHistogramH(line, bins=line.shape[0])
    Max = np.where(Histogram == max(Histogram))[0]

    Max = Max[0]
    return Max

# good result at thrs 50 then rotate then thrs 100
img = loadImage('test.png')
img = invertImage(img)
binaryImg = blackAndWhite(img, thrs = 50)
angle = fixSkewAngle(binaryImg)
# showImage(binaryImg)
# exit()
img = rotateImage(img, angle=angle)
img = blackAndWhite(img, thrs = 100)
# showImage(img)
Lines = seperateLines(img)
# for Line in Lines:
#     Baseline = getBaseLine(Line)
#     Points = [(Baseline, X) for X in range(Line.shape[1])]
#     showImageZoomed(Line, ratio=2, points=Points)

def seperateParts(img):
    img = img.copy()

    def getPartPixels(point):
        Directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        if -1 < point[0] < img.shape[0] and -1 < point[1] < img.shape[1]:
            pass
        else:
            return []

        if img[point[0], point[1]] != 255:
            return []
        else:
            img[point[0], point[1]] = 0
            Pixels = [point]
            for Dir in Directions:
                Pixels = Pixels + getPartPixels(elementwiseAdding(point, Dir))
            return Pixels

    Parts = []
    # showImage(img)
    WhitePixels = np.where(img == 255)
    while len(WhitePixels[0]) != 0:
        FirstWhitePixel = (WhitePixels[0][0] , WhitePixels[1][0])
        Copy = np.zeros(img.shape, np.uint8)
        Pixels = getPartPixels(FirstWhitePixel)
        for index in range(len(Pixels)):
            Copy[Pixels[index][0], Pixels[index][1]] = 255
        # showImage(Copy)
        Parts.append(Copy)
        # print(Pixels)
        WhitePixels = np.where(img == 255)  
    return Parts

def seperateWordsV2(line):
    line = removePadding(line)
    Baseline = getBaseLine(line)
    
    VHistogram = getHistogramV(line, bins=line.shape[1])
    VHistogramZeros = list(np.where(VHistogram == 0)[0])
    VHistogramZeros.append(img.shape[1] + 50) # dump value to add last interval
    StartInterval = -1
    EndInterval = -1
    ZerosIntervals = []
    for Value in VHistogramZeros:
        if StartInterval == -1:
            StartInterval = Value
            EndInterval = Value
        elif Value - EndInterval == 1:
            EndInterval = Value
        elif Value - EndInterval > 1:
            ZerosIntervals.append((StartInterval, EndInterval))
            StartInterval = Value
            EndInterval = Value

    SpaceSizes = [End - Start + 1 for Start, End in ZerosIntervals]
    SpaceAvg = sum(SpaceSizes) / len(SpaceSizes)
    Words = []
    WordStart = 0
    for Start, End in ZerosIntervals:
        if End - Start + 1 > SpaceAvg:
            Words.append(line[:, WordStart: Start])
            WordStart = End + 1
            
    Words.append(line[:, WordStart:])
    return Words, Baseline

def getLettersSeperators(img, baseline):

    thin = zhangSuen(img)
    SupportHeight = 4

    def isValidSeperator(x):
        if thin[baseline, x] != 255: return False
        LonelyPixel = all([Pixel == 0 for Pixel in thin[: baseline, x]] + [Pixel == 0 for Pixel in thin[baseline + 1: , x]])
        return LonelyPixel
        
        if not LonelyPixel: return False
        if x - 1 > 0 and thin[baseline, x - 1] == 255:
            LeftSupport = all([Pixel == 0 for Pixel in thin[baseline - SupportHeight: baseline, x - 1]] + [Pixel == 0 for Pixel in thin[baseline + 1: baseline + SupportHeight + 1, x - 1]])
            if LeftSupport: return True
        if x + 1 < thin.shape[1] and thin[baseline, x + 1] == 255:
            RightSupport = all([Pixel == 0 for Pixel in thin[baseline - SupportHeight: baseline, x + 1]] + [Pixel == 0 for Pixel in thin[baseline + 1: baseline + SupportHeight + 1, x + 1]])
            if RightSupport: return True
        return False

    SeperationPointsX = [X for X in range(img.shape[1]) if isValidSeperator(X)]
    SeperationPointsX = SeperationPointsX + [thin.shape[1] + 50] # dump value to add last interval
    Seperators = []
    Start = SeperationPointsX[0]
    End = SeperationPointsX[0]
    for X in SeperationPointsX[1:]:
        if X - End > 1:
            if Start != 0 and sum(thin[baseline, 0: Start]) != 0: # not the first pixel in the baseline
                Seperators.append((Start, End))
            Start = X
        End = X
        
    return Seperators

def lettersSeperatorsToParts(parts, seperators, baseline):

    def getXBoundries(img):
        Xs = np.where(img == 255)[1]
        return min(Xs), max(Xs)

    def getRelativeBasePosition(img):
        Baseline = img[baseline - 1: baseline + 2, :]
        FirstPixelY = np.where(img == 255)[0][0]
        if Baseline.any() != 0:
            return 'onbase'
        elif FirstPixelY < baseline - 1:
            return 'abovebase'
        else:
            return 'underbase'

    NewParts = []
    Info = []       # {boundries(xFrom, xTo), boundries-noseperators(xFrom, xTo), position(isolated| begining| middle| ending), base(underbase, abovebase, onbase)}
    for Idx, Part in enumerate(Parts):
        Thin = zhangSuen(Part)
        if len(np.where(Thin == 255)[0]) != 0:
            Part = Thin
        Seperators = [(0, 0)] + seperators[Idx] + [(Part.shape[1] - 1, Part.shape[1] - 1)]
        for SIdx in range(len(Seperators) - 1):
            Start1 = Seperators[SIdx][0]
            End1 = Seperators[SIdx][1]
            Start2 = Seperators[SIdx + 1][0]
            End2 = Seperators[SIdx + 1][1]
            NewPart = Part[:, Start1: End2 + 1]
            NewPart = addPadding(NewPart, (0, 0, Start1, Part.shape[1] - End2 - 1))
            NewParts.append(NewPart)
            XFrom, XTo = getXBoundries(NewPart)
            if len(Seperators) == 2:    # isolated
                Info.append({
                    'boundries': (XFrom, XTo),
                    'boundries-noseperators': (XFrom, XTo),
                    'position': 'isolated',
                    'base': getRelativeBasePosition(NewPart)
                })
            elif SIdx == 0:             # ending
                Info.append({
                    'boundries': (XFrom, XTo),
                    'boundries-noseperators': (XFrom, Start2),
                    'position': 'ending',
                    'base': 'onbase'
                })
            elif SIdx == len(Seperators) - 2:   # begining
                Info.append({
                    'boundries': (XFrom, XTo),
                    'boundries-noseperators': (End1, XTo),
                    'position': 'begining',
                    'base': 'onbase'
                })
            else:                               # middle
                Info.append({
                    'boundries': (XFrom, XTo),
                    'boundries-noseperators': (End1, Start2),
                    'position': 'middle',
                    'base': 'onbase'
                })

    return NewParts, Info

def combineLettersWithDots(parts, info):
    
    def getXBoundries(img):
        Xs = np.where(img == 255)[1]
        return min(Xs), max(Xs)

    NewParts = []
    Info = []
    for PIdx, Part in enumerate(parts):
        PInfo = info[PIdx]
        if PInfo['base'] == 'onbase':
            SubParts = []
            for SPIdx, SubPart in enumerate(parts):
                SPInfo = info[SPIdx]
                SPCenter = (SPInfo['boundries'][0] + SPInfo['boundries'][1]) / 2
                if SPInfo['base'] != 'onbase' and SPCenter >= ((PInfo['boundries'][0] + PInfo['boundries-noseperators'][0]) // 2) and \
                        SPCenter <= (\
                        ((PInfo['boundries'][1] + PInfo['boundries-noseperators'][1] - 1) // 2) if PInfo['boundries'][1] != PInfo['boundries-noseperators'][1] else PInfo['boundries'][1]):
                    SubParts.append(SubPart)
            NewPart = Part
            for SubPart in SubParts:
                NewPart = np.add(NewPart, SubPart)
            NewParts.append(NewPart)
            XFrom, XTo = getXBoundries(NewPart)
            Info.append({
                'boundries': (XFrom, XTo),
                'boundries-noseperators': PInfo['boundries-noseperators'],
                'position': PInfo['position'],
                'base': 'onbase'
            })

    return NewParts, Info

Lines = [seperateWordsV2(Line) for Line in Lines]
for Line, Baseline in Lines:
    for Word in reversed(Line):
        Parts = seperateParts(Word)
        BaseLinePoints = [(Baseline, X) for X in range(Word.shape[1])]
        showMultipleImages(Parts, waitkey=False, name='word', points=BaseLinePoints)

        LettersSeperators = [getLettersSeperators(Part, Baseline) for Part in Parts]
        # print(LettersSeperators)
        # closeAllWindows()

        Parts, Info = lettersSeperatorsToParts(Parts, LettersSeperators, Baseline)
        print(Info)
        showMultipleImages(Parts, name='seperated', waitkey=False)
        print()
        Parts, Info = combineLettersWithDots(Parts, Info)
        print(Info)
        showMultipleImages(Parts, name='seperated combined', waitkey=False)
        print('#' * 15)
        closeAllWindows()
        # thin = addPadding(Word, 1, 1)
        # thin = zhangSuen(thin)
        # thin = removePadding(thin, padding=(1, 1))
        # showImageZoomed(thin, ratio=10, points=Points, waitkey=False, name='Thin')
        # showImageZoomed(Word, ratio=10, points=Points, name='Original')
