import cv2
import numpy as np
from FeaturesExtractor import *

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

    # HistogramAvg = sum(Histogram) / len(Histogram)
    # [print(Idx, H) for Idx, H in enumerate(Histogram)]
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
            # print('M', MaxInterval)
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
    # print(Seperators)
    # Points = []
    # for Line in Seperators:
    #     Points += [(Line, X) for X in range(img.shape[1])]
    # showImage(img, points=Points)

    # Seperators = [(LocalMaximums[Idx] + LocalMaximums[Idx - 1]) // 2 for Idx in range(1, len(LocalMaximums))]

    # print(Seperators)
    # Points = []
    # for Line in Seperators:
    #     Points += [(Line, X) for X in range(img.shape[1])]
    # showImage(img, points=Points)

def getBaseLine(line):
    Histogram = getHistogramH(line, bins=line.shape[0])
    Max = np.where(Histogram == max(Histogram))[0]

    if len(Max) > 1: print(Max)
    # print(Histogram)
    Max = Max[0]
    return Max

# good result at thrs 50 then rotate then thrs 100
img = loadImage('test.png')
img = invertImage(img)
binaryImg = blackAndWhite(img, thrs = 50)
angle = fixSkewAngle(binaryImg)
showImage(binaryImg)
# exit()
img = rotateImage(img, angle=angle)
img = blackAndWhite(img, thrs = 100)
showImage(img)
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
    # Points = [(Baseline, X) for X in range(line.shape[1])]
    # showImageZoomed(line, ratio=1, points=Points)
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
    # print(ZerosIntervals)
    SpaceSizes = [End - Start + 1 for Start, End in ZerosIntervals]
    # DistnictSpaceSizes = list(set(SpaceSizes))
    # print(sum(SpaceSizes) / len(SpaceSizes))
    # print(sum(DistnictSpaceSizes) / len(DistnictSpaceSizes))
    SpaceAvg = sum(SpaceSizes) / len(SpaceSizes)
    # print(SpaceSizes)
    # print(SpaceAvg)
    Words = []
    WordStart = 0
    for Start, End in ZerosIntervals:
        if End - Start + 1 > SpaceAvg:
            Words.append(line[:, WordStart: Start])
            WordStart = End + 1
            # line[:, Start: End + 1] = 125
    # showImageZoomed(line, ratio=1, points=Points)
    Words.append(line[:, WordStart:])
    return Words, Baseline
    
from thin import *
Lines = [seperateWordsV2(Line) for Line in Lines]
for Line, Baseline in Lines:
    for Word in reversed(Line):
        Parts = seperateParts(Word)
        Points = [(Baseline, X) for X in range(Word.shape[1])]
        showMultipleImages(Parts, points=Points)
        # thin = addPadding(Word, 1, 1)
        # thin = zhangSuen(thin)
        # thin = removePadding(thin, padding=(1, 1))
        # showImageZoomed(thin, ratio=10, points=Points, waitkey=False, name='Thin')
        # showImageZoomed(Word, ratio=10, points=Points, name='Original')


def seperateWords(img, flag = 125, getLines = False):
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
    for wIndex, Img in enumerate(Images):
        if getLines:
            WordsImages.append([])
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
                if getLines:
                    WordsImages[wIndex].append(Img[:, ImgEnded + 1:ImgStarted + 1])
                else:
                    WordsImages.append(Img[:, ImgEnded + 1:ImgStarted + 1])
                ImgStarted = -1
                ImgEnded = -1
    return WordsImages if getLines else WordsImages, Images

def seperateLetters(img, baseline):

    def checkSeperation(baseline, x):
        if not (img[baseline, x] == 255 and (img[baseline, x - 1] == 255 or img[baseline, x + 1] == 255)): return False
        VerticalHeight = 3
        for dY in range(-1 * baseline, img.shape[0] - 1 - baseline):
            if dY == 0: continue
            if not (img[baseline + dY, x] == 0):
                return False
        # SupportRight = True
        # for dY in range(-1 * VerticalHeight, VerticalHeight):
        #     if dY == 0: continue
        #     if not (img[baseline + dY, x + 1] == 0):
        #         SupportRight = False
        #         break
        # SupportLeft = True
        # for dY in range(-1 * VerticalHeight, VerticalHeight):
        #     if dY == 0: continue
        #     if not (img[baseline + dY, x - 1] == 0):
        #         SupportLeft = False
        #         break
        # return SupportRight or SupportLeft
        return True

    Points = [(baseline, X) for X in range(1, img.shape[1] - 1) if checkSeperation(baseline, X)]
    showImageZoomed(img, points=Points, name='letters', waitkey=False)

    if len(Points) == 0:
        showImageZoomed(img, waitkey=False, name=str(0))
        closeAllWindows()
        return [img]

    Seperators = []
    Start = Points[0][1]
    End = Points[0][1] - 1
    for Point in Points:
        if End == Point[1] - 1:
            End = Point[1]
        else:
            Seperators.append((Start, End))
            Start = Point[1]
            End = Start
    Seperators.append((Start, End))

    Letters = []

    print(len(Seperators))
    print(Seperators)

    if Points[0][1] != min(np.where(img == 255)[1]):
        # Start2 = Seperators[0][0]
        End2 = Seperators[0][1]
        Letter = img[:, 0: End2 + 1]

        # Letter[0: baseline, Start2: End2 + 1] = 0
        # Letter[baseline + 1:, Start2: End2 + 1] = 0
        
        Letters.append(Letter)

    for Idx in range(len(Seperators) - 1):
        Start1 = Seperators[Idx][0]
        # End1 = Seperators[Idx][1]
        # Start2 = Seperators[Idx + 1][0]
        End2 = Seperators[Idx + 1][1]
        
        Letter = img[:, Start1: End2 + 1]

        # Letter[0: baseline, 0: (End1 - Start1) + 1] = 0
        # Letter[baseline + 1:, 0: (End1 - Start1) + 1] = 0
        
        # Letter[0: baseline, (Start2 - Start1): (End2 - Start1) + 1] = 0
        # Letter[baseline + 1:, (Start2 - Start1): (End2 - Start1) + 1] = 0
        
        Letters.append(Letter)

    Start1 = Seperators[-1][0]
    # End1 = Seperators[-1][1]
    # Start2 = img.shape[1] - 1
    End2 = img.shape[1] - 1
    Letter = img[:, Start1: End2 + 1]

    # Letter[0: baseline, 0: (End1 - Start1) + 1] = 0
    # Letter[baseline + 1:, 0: (End1 - Start1) + 1] = 0
    
    Letters.append(Letter)
    # [showImageZoomed(Letter, waitkey=False, name=str(Idx)) for Idx, Letter in enumerate(Letters)]
    # closeAllWindows()
    # showImageZoomed(Letters[1], name='fdvf', waitkey=False)

    CorrectedLetters = []
    for Letter in Letters:
        # showImageZoomed(Letter, name='fdvf')
        Parts = seperateToParts(Letter)
        print(len(Parts))
        ChoosenPart = Parts[0]
        # showImageZoomed(ChoosenPart, name='fdvfd')
        for Part in Parts[1:]:
            if (len(np.where(Part == 255)[0]) / (Letter.shape[0] * Letter.shape[1])) > (len(np.where(ChoosenPart == 255)[0]) / (Letter.shape[0] * Letter.shape[1])):
                ChoosenPart = Part
        CorrectedLetters.append(ChoosenPart)

    CorrectedLetters = [addPadding(Letter, 0, 10) for Letter in CorrectedLetters]
    [showImageZoomed(Letter, waitkey=False, name=str(Idx)) for Idx, Letter in enumerate(CorrectedLetters)]
    closeAllWindows()
