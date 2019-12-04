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
    # print(angle)
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return img

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
        SupportRight = True
        for dY in range(-1 * VerticalHeight, VerticalHeight):
            if dY == 0: continue
            if not (img[baseline + dY, x + 1] == 0):
                SupportRight = False
                break
        SupportLeft = True
        for dY in range(-1 * VerticalHeight, VerticalHeight):
            if dY == 0: continue
            if not (img[baseline + dY, x - 1] == 0):
                SupportLeft = False
                break
        return SupportRight or SupportLeft

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
