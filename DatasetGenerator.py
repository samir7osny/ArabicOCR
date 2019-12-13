from Preprocessing import *
from Utilities import *
import os
from ClassesMap import *

LogFile = open('log.txt', 'w', encoding='utf-8')

Path = 'CharactersDataset/'
ImagesNames = []
for r, d, f in os.walk(Path):
    ImagesNames.extend([file for file in f if file[-4: ] == '.png'])
    break

NotIncludedPath = 'CharactersDataset/Letters/NotIncluded/'
if not os.path.isdir(NotIncludedPath):
    os.mkdir(NotIncludedPath)
    
WrongSegmentedPath = 'CharactersDataset/Letters/WrongSegmented/'
if not os.path.isdir(WrongSegmentedPath):
    os.mkdir(WrongSegmentedPath)

FaultsPath = 'CharactersDataset/Letters/Faults/'
if not os.path.isdir(FaultsPath):
    os.mkdir(FaultsPath)

Total = 0
for ImageName in ImagesNames:
    LogFile.write('Image ' + ImageName[ :-4])
    LogFile.write('\n')
    # if ImageName != 'capr1265.png': continue
    TextName = ImageName[:-3] + 'txt'
    WordIdx = 0
    Text = (open(Path + TextName, 'r', encoding='utf-8')).read()
    TextWords = Text.split(' ')
    TextWords = [Word.replace(' ', '').replace('\n', '') for Word in TextWords if Word.replace(' ', '').replace('\n', '') != '']
    # print(len(TextWords))
    Img = loadImage(Path + ImageName)
    Img = invertImage(Img)
    Angle = fixSkewAngleV2(Img)
    LogFile.write('Angle ' + str(Angle))
    LogFile.write('\n')
    # Angle = 0
    Img = rotateImage(Img, angle=Angle)
    Img = blackAndWhite(Img, thrs=100)

    # showImage(Img)

    LogFile.write('Preprocessing completed.')
    LogFile.write('\n')

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
            Total += 1
            # Seperate To Parts
            Parts = seperateParts(Word)
            
            LettersSeperators = [getLettersSeperators(Part, Baseline) for Part in Parts]
            Parts, Info = lettersSeperatorsToParts(Parts, LettersSeperators, Baseline)

            # showMultipleImages(Parts)
            
            for idx, I in enumerate(Info):
                Info[idx]['img'] = Parts[idx]

            Info = sorted(Info, key=lambda x:x['boundries'][0], reverse=True)

            if WordIdx >= len(TextWords): break
            Length = len(TextWords[WordIdx])
            Lam = False
            for C in TextWords[WordIdx]:
                if C == 'ل':
                    Lam = True
                elif C == 'ا' and Lam:
                    Length -= 1
                    Lam = False
                else:
                    Lam = False
            if len([_ for Part in Info if Part['base'] == 'onbase']) != Length:
                LogFile.write(TextWords[WordIdx] + ' ' + str(len([_ for Part in Info if Part['base'] == 'onbase'])) + ' ' + str(Length))
                LogFile.write('\n')
                Count = 0
                WordText = TextWords[WordIdx].replace('.', 'dot').replace(':', 'tdots').replace('،', 'coma')
                if not os.path.isdir(WrongSegmentedPath + WordText + '/'):
                    os.mkdir(WrongSegmentedPath + WordText + '/')
                    Dir = WrongSegmentedPath + WordText + '/'
                    for Part in [P for P in Info if P['base'] == 'onbase']:
                        Img = Part['img']
                        Img = centeralizeTheLetter(Img, Baseline)
                        Img = resizeByPadding(Img, (50, 50))
                        cv2.imwrite(Dir + str(Count) + '.png', Img)
                        Count += 1
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
                    
                    Letter = TextWords[WordIdx][LetterIdx] + TextWords[WordIdx][LetterIdx + 1] if LetterIdx + 1 < len(TextWords[WordIdx]) and TextWords[WordIdx][LetterIdx] == 'ل' and TextWords[WordIdx][LetterIdx + 1] == 'ا' else TextWords[WordIdx][LetterIdx]
                    if len(Letter) == 2: LetterIdx += 1
                    if Letter not in Letters: 
                        LogFile.write('not included in letters ' + Letter + '\t\t' + TextWords[WordIdx])
                        LogFile.write('\n')
                        Duplicates = 0
                        while os.path.isfile(NotIncludedPath + str(Duplicates) + '.png'):
                            Duplicates += 1
                        cv2.imwrite(NotIncludedPath + str(Duplicates) + '.png', Img)
                        LetterIdx += 1
                        continue

                    try:
                        Class = Letters[Letter]['seqs'][Position][0][0][1] + 1
                    except:
                        LogFile.write('fault ' + str(LetterIdx) + ' ' + Letter + ' ' + str(Position) + ' ' + TextWords[WordIdx] + ' ' + str(Letters[Letter]['seqs']))
                        LogFile.write('\n')
                        WordText = TextWords[WordIdx].replace('.', 'dot').replace(':', 'tdots').replace('،', 'coma')
                        FaultsPath
                        if not os.path.isdir(FaultsPath + WordText + '/'):
                            os.mkdir(FaultsPath + WordText + '/')
                            Dir = FaultsPath + WordText + '/'
                            for Part in [P for P in Info if P['base'] == 'onbase']:
                                Img = Part['img']
                                Img = centeralizeTheLetter(Img, Baseline)
                                Img = resizeByPadding(Img, (50, 50))
                                cv2.imwrite(Dir + str(Count) + '.png', Img)
                        break
                        # showImageZoomed(Word, waitkey=False)
                        # showImageZoomed(Img, name='char')
                        # exit()

                    LogFile.write(Letter + ' ' +  Char + str(Class))
                    LogFile.write('\n')
                    # showImageZoomed(Img)

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
                
LogFile.write(str(Total))
LogFile.write('\n')
LogFile.close()