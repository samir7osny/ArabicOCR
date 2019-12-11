from Utilities import *
from Preprocessing import *
from HOGV3 import getHOG
from Thining import zhangSuen
from Classification import Classifier
import os
import time

clf = Classifier()

# good result at thrs 50 then rotate then thrs 100
img = loadImage('test.png')
img = invertImage(img)
binaryImg = blackAndWhite(img, thrs = 50)
Start = time.time()
angle = fixSkewAngleV2(binaryImg)
print(time.time() - Start)
# showImage(binaryImg)
# exit()
img = rotateImage(img, angle=angle)
# img = cv2.resize(img, (img.shape[0] * 2, img.shape[1] * 2))
img = blackAndWhite(img, thrs = 112)

First = min(np.where(img == 255)[0])
Points = [(First, X) for X in range(img.shape[1])]
# showImage(img, points=Points)

Lines = seperateLines(img)
path = 'LBaseline/'
# for Line in Lines:
#     Baseline = getBaseLine(Line)
#     Points = [(Baseline, X) for X in range(Line.shape[1])]
#     showImageZoomed(Line, ratio=2, points=Points)
Lines = [seperateWords(Line) for Line in Lines]
for Line, Baseline in Lines:
    for Word in Line[::-1]:
        Parts = seperateParts(Word)
        BaseLinePoints = [(Baseline, X) for X in range(Word.shape[1])]
        # showMultipleImages([zhangSuen(Part) for Part in Parts], name='word', points=BaseLinePoints)

        LettersSeperators = [getLettersSeperators(Part, Baseline) for Part in Parts]
        # SeperatePoints = []
        # for PartSeperator in LettersSeperators:
        #     for LettersSeperator in PartSeperator:
        #         Center = (LettersSeperator[0] + LettersSeperator[1]) // 2
        #         SeperatePoints += [(Y, Center) for Y in range(Word.shape[0])]
        # showImageZoomed(zhangSuen(Word), points=SeperatePoints, name='seperators')

        Parts, Info = lettersSeperatorsToParts(Parts, LettersSeperators, Baseline)
        # print(Count)
        Parts = Parts[::-1]
        Info = Info[::-1]
        # print(Info)
        for idx, I in enumerate(Info):
            Info[idx]['img'] = Parts[idx]
        Info = sorted(Info, key=lambda x:x['boundries'][0], reverse=True)

        for Part in Info:
            # Idx = len(Parts) - 1 - Idx
            img = Part['img']
            if Part['base'] == 'onbase':
                # img = removePadding(img)  
                # PPart = resizeByPadding(Part, (100, 100))
                print(Part['position'])
                # clf.predict(img, Part['position'])
                showImageZoomed(img, points=BaseLinePoints, waitkey=False, name='1')
                img = centeralizeTheLetter(img, Baseline)
                LetterBaseLine = img.shape[0] // 2
                LetterBaseLinePoints = [(LetterBaseLine, X) for X in range(img.shape[1])]
                print(img.shape)
                img = resizeByPadding(img, (50, 50))
                showImageZoomed(img, waitkey=False)

                # Char = 'S'
                # if Part['position'] == 'ending': Char = 'E'
                # if Part['position'] == 'middle': Char = 'M'
                # if Part['position'] == 'beginning': Char = 'B'

                # Count = 0
                # Index = input('Index: ')
                # while os.path.isfile(path + Char + str(Index) + '_' + str(Count) + '.png'):
                #     Count += 1

                # cv2.imwrite(path + Char + str(Index) + '_' + str(Count) + '.png', img)
                closeAllWindows(waitkey=True)