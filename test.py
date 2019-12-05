from thin import *
from Preprocessing import *
from FeaturesExtractor import *
from Utilities import *
from math import sqrt

def distance(a, b):
    assert len(a) == len(b) == 2
    return sqrt(    (a[0] - b[0])**2    +   (a[1] - b[1])**2    )

def getLineSegments(img):
    # Directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    # Lines = []
    # Visited = np.zeros(img.shape)
    # WhitePixels = np.where(img == 255)
    # WhitePixels = [(WhitePixels[0][Index], WhitePixels[1][Index]) for Index in range(len(WhitePixels[0]))]
    # NotVisited = WhitePixels.copy()

    # LinePixels = [NotVisited.pop(0)]
    # Line = [()]
    # while len(NotVisited) != 0:
    #     CurrentP1 = Line[-1]
    #     Adj = [elementwiseAdding(CurrentP1, Dir) for Dir in Directions if elementwiseAdding(CurrentP1, Dir) in WhitePixels]
    #     Distances = [distance(CurrentP1, Point) for Point in Adj]
    #     print(Distances)      
    #     print(np.where(Distances == min(Distances)))
    #     exit()
    zeros = img[img != 255]
    lines = cv2.HoughLinesP(img, 1, np.pi / 1, 0, minLineLength=3)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    print(lines)
    if lines is not None:
        for index, line in enumerate(lines):
            # print(line)
            x1, y1, x2, y2 = line[0]
            temp = (index + 1) * (1 / lines.shape[0]) * 255
            cv2.line(img,(x1,y1),(x2,y2),(0,temp,0),1)
        showImageZoomed(img)

def getLinePixels(line):
    pass

# img = loadImage('test.png')
# img = fixSkew(img)
# img = invertImage(img)
# img = blackAndWhite(img)
# words = seperateWords(img)
# nword = 28
# nword = 4
# # showImageZoomed(words[nword])
# parts = seperateToParts(words[nword])


# npart = 1
# npart = 0
# # showImageZoomed(parts[npart], waitkey = False, name='original')
# # print(parts[npart].shape)
# part = addPadding(parts[npart], 1, 1)
# part[part <= 100] = 0
# part[part > 0] = 1
# thin = zhangSuen(part)

# thin[thin != 0] = 255
# showImageZoomed(thin, waitkey = False, name='thin')
# closeAllWindows();
# Lines = getLineSegments(thin)


img = loadImage('test.png')
# img = invertImage(img)
# showImage(img)
# img[:, :] = img[:, :] * 1.5
# kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
# img = cv2.filter2D(img, -1, kernel)

# cv2.imwrite('test2.png', img)
# showImage(img)
# exit()
img = invertImage(img)
img = fixSkew(img, thrs=50)
img = blackAndWhite(img, thrs=90)
words, lines = seperateWords(img, getLines = True)
LineIndex = 3
line = lines[LineIndex]
showImage(line)
# showImage(line)
words = words[LineIndex]
line[line < 150] = 0
line = addPadding(line, 1, 1)
line = cv2.flip(line, 1)
line = zhangSuen(line)
line = cv2.flip(line, 1)
# showImage(line, name='dvdf')

# print(line.shape)

# showImageZoomed(line, name='dvdf')

bins = line.shape[0]
Histogram = getHistogramH(line, bins=bins)
Maxima = np.where(Histogram == max(Histogram))[0][0] - 1
# showImageZoomed(line, points=[(Maxima + 1, X) for X in range(line.shape[1])])

for word in (words):
    showImageZoomed(word, name='word', waitkey=False)
    # print(word.shape)
    parts = seperateToParts(word)
    for part in parts:
        if len(np.where(part == 255)[0]) / (part.shape[0] * part.shape[1]) <= 0.05: continue
        part = addPadding(part, 1, 1)
        
        part = cv2.flip(part, 1)
        thin = zhangSuen(part)
        thin = cv2.flip(thin, 1)
        
        showImageZoomed(thin, points=[(Maxima + 1, X) for X in range(thin.shape[1])], waitkey=False, name='part')
        closeAllWindows()
        seperateLetters(thin, baseline=Maxima + 1)

# nword = 28
# nword = 4
# # showImageZoomed(words[nword])
# parts = seperateToParts(words[nword])


# npart = 1
# npart = 0
# # showImageZoomed(parts[npart], waitkey = False, name='original')
# # showImageZoomed(parts[npart], points=[(Maxima, X) for X in range(parts[npart].shape[1])])
# part = addPadding(parts[npart], 1, 1)
# thin = zhangSuen(part)
# showImageZoomed(thin, points=[(Maxima + 1, X) for X in range(thin.shape[1])])

# seperateLetters(thin, baseline=Maxima + 1)