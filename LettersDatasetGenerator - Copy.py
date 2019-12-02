import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
from textSupport import *

FontsDir = 'GFonts'
FontsFiles = []
for (_, _, FileNames) in os.walk(FontsDir):
    FontsFiles.extend(FileNames)
    break

DatasetDir = 'LettersDataset'

# 064A
LettersFile = open('Letters', 'r')
LettersFileText = LettersFile.read()
LettersFile.close()
LettersFileText = LettersFileText[:LettersFileText.rfind('#')]
Letters = LettersFileText.split('\n')
for Index, Letter in enumerate(Letters):
    Letters[Index] = [Input for Input in Letter.split(' ') if Input.replace(' ', '') != '']
print(Letters)
#Copy 
for integer in range(int(u'0627', 16), int(u'0628', 16) + 1):

    string = str(integer)
    character = chr(integer)

    if os.path.isdir(DatasetDir + '/' + string) is False:
        os.mkdir(DatasetDir + '/' + string)

    for FontFile in FontsFiles:
        for Prefix, Text in [('Isolated', character), 
            ('End', 'ـ' + character),
            ('Beginning', character + 'ـ'),
            ('Middle', 'ـ' + character + 'ـ')]:
            Text = arabic_reshaper.reshape(Text)
            Text = get_display(Text, base_dir='R')

            if isTextSupported(FontsDir + '/' + FontFile, Text) is False:
                continue

            W, H = 500, 250
            Font = ImageFont.truetype(FontsDir + '/' + FontFile, 100)
            Img = Image.new("RGB", (W, H),(255,255,255))
            Draw = ImageDraw.Draw(Img)
            w, h = Draw.textsize(Text, Font)

            Draw.text(((W - w) / 2, (H - h) / 2), Text, (0,0,0), font = Font)
            Draw = ImageDraw.Draw(Img)
                
            if os.path.isdir(DatasetDir + '/' + string + '/' + Prefix) is False:
                os.mkdir(DatasetDir + '/' + string + '/' + Prefix)
                
            Img.save(DatasetDir + '/' + string + '/' + Prefix + '/' + FontFile[:FontFile.rfind('.')] + ".png")