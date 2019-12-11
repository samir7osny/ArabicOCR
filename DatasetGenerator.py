from Preprocessing import *
from Utilities import *
import os
from ClassesMap import *

Path = 'CharactersDataset/'
ImagesNames = []
for r, d, f in os.walk(Path):
    ImagesNames.extend([file for file in f if file[-4: ] == '.png'])
    break

for ImageName in ImagesNames:
    if ImageName != 'caug1463.png': continue
    TextName = ImageName[:-3] + 'txt'
    WordIdx = 0
    Text = (open(Path + TextName, 'r', encoding='utf-8')).read()
    TextWords = Text.split(' ')
    TextWords = [Word for Word in TextWords if Word.replace(' ', '').replace('\n', '') != '']
    # print(len(TextWords))
    Img = loadImage(Path + ImageName)
    Img = invertImage(Img)
    Angle = fixSkewAngleV2(Img)
    # Angle = 0
    Img = rotateImage(Img, angle=Angle)
    Img = blackAndWhite(Img, thrs=100)

    # Seperate To Lines
    Lines = seperateLines(Img)
    # Seperate To Words
    Lines = [seperateWords(Line) for Line in Lines]
    Words = []
    for Line, _ in Lines:
        for Word in Line[::-1]:
            Words.append(Word)

    NWords = len(Words)
    # print(NWords)

    # for Idx in range(len(Words)):
    #     print(Idx + 1, TextWords[Idx])
    #     showImageZoomed(Words[Idx])
    WordIdx = 0
    for Line, Baseline in Lines:
        for Word in Line[::-1]:
            # Seperate To Parts
            Parts = seperateParts(Word)
            
            LettersSeperators = [getLettersSeperators(Part, Baseline) for Part in Parts]
            Parts, Info = lettersSeperatorsToParts(Parts, LettersSeperators, Baseline)

            showMultipleImages(Parts)
            
            for idx, I in enumerate(Info):
                Info[idx]['img'] = Parts[idx]

            Info = sorted(Info, key=lambda x:x['boundries'][0], reverse=True)

            if len([_ for Part in Info if Part['base'] == 'onbase']) != len(TextWords[WordIdx]):
                print(TextWords[WordIdx], len([_ for Part in Info if Part['base'] == 'onbase']), len(TextWords[WordIdx]))
                for Part in Info:
                    showImageZoomed(Part['img'])
                WordIdx += 1
                continue

            LetterIdx = 0
            for Part in Info:
                Img = Part['img']

                if Part['base'] == 'onbase':
                    # BaseLinePoints = [(Baseline, X) for X in range(Img.shape[1])]
                    # showImageZoomed(Img, points=BaseLinePoints, waitkey=False, name='Word')

                    Img = centeralizeTheLetter(Img, Baseline)
                    # LetterBaseLine = Img.shape[0] // 2
                    # LetterBaseLinePoints = [(LetterBaseLine, X) for X in range(Img.shape[1])]
                    
                    Img = resizeByPadding(Img, (50, 50))
                    # showImageZoomed(Img, waitkey=False)
                    
                    # closeAllWindows(waitkey=True)

                    # Save the Images
                    
                    Char = 'S'
                    Position = ISOLATED
                    if Part['position'] == 'ending': 
                        Char = 'E'
                        Position = END
                    if Part['position'] == 'middle': 
                        Char = 'M'
                        Position = MIDDLE
                    if Part['position'] == 'beginning': 
                        Char = 'B'
                        Position = BEGINNING
                    
                    Letter = TextWords[WordIdx][LetterIdx]
                    if Letter not in Letters: 
                        print('not included in letters ', Letter)
                        LetterIdx += 1
                        continue

                    Class = Letters[Letter]['seqs'][Position][0][0][1] + 1

                    print(Letter)
                    print(Char + str(Class))
                    showImageZoomed(Img)

                    Duplicates = 0
                    FileName = Char + str(Class) + '_' + str(Duplicates) + '.png'

                    LetterPath = Path + 'Letters/' + ImageName[:-3] + '/'
                    if not os.path.isdir(LetterPath):
                        os.mkdir(LetterPath)
                    while os.path.isfile(LetterPath + FileName):
                        FileName = Char + str(Class) + '_' + str(Duplicates) + '.png'
                        Duplicates += 1
                    LetterIdx += 1

                    cv2.imwrite(LetterPath + FileName, Img)                    

            WordIdx += 1
                

