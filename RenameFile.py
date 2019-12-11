from Utilities import *
import cv2
from os import walk, remove
mypath = 'L'
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break

for file in f:
    img = cv2.imread('L/' + file)
    showImageZoomed(img)
    name = input('name: ')
    remove('L/' + file)
    cv2.imwrite('L/' + name + '.png', img)