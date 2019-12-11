import os
import cv2
from Utilities import *

path = 'L/'
path = 'L2/'
files = []
for r, d, f in os.walk(path):
    files.extend(f)
    break

# path = 'L2/'

# for file in files:
#     img = loadImage('L/' + file)
#     img = resizeByPadding(img, (100, 100))
#     cv2.imwrite('L2/' + file, img)

def absDiff(img1, img2):
    assert img1.shape[0] == img2.shape[0] and img1.shape[1] == img2.shape[1], str(img1.shape) + ' ' + str(img2.shape)
    # print(str(img1.shape) + ' ' + str(img2.shape))
    Diff = abs(img1 - img2)
    return sum(sum(Diff))

images = []
for file in files:
    img = loadImage('L2/' + file)
    images.append(img)

Diffs = []
for Idx, Img in enumerate(images):
    print(files[Idx])
    Diffs.append([])
    for Idx2, Img2 in enumerate(images):
        if Idx == Idx2: continue
        Diffs[Idx].append((absDiff(Img, Img2), files[Idx2]))
    Diffs[Idx] = sorted(Diffs[Idx], key=lambda x: x[0])
    print(Diffs[Idx])
    print()
