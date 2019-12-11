
import numpy as np
from sklearn.svm import SVC
from ClassesMap import *
from Utilities import *
import os
from HOGV3 import getHOG
from math import sqrt
from FeaturesExtractor import *

class DiffClassifier(object):
    def __init__(self):
        self.data = []
        self.classes = []
    
    def fit(self, X, y):
        assert len(X) == len(y)
        self.data = X
        self.classes = y

    def predict(self, img):
        img = img[0]
        img = img.astype(np.float64)
        Diffs = []

        for Idx, DImg in enumerate(self.data):
            DImg = DImg.astype(np.float64)
            Diffs.append((self.classes[Idx], sum(sum(abs(img - DImg)))))
        # print(Diffs)
        Diffs = sorted(Diffs, key=lambda x: x[1])
        # if Diffs[0][0] == 51:
        #     idx = self.classes.index(51)
        #     idx2 = self.classes.index(53)
        #     showImageZoomed(abs(self.data[idx] - img), name='diff1')
        #     showImageZoomed(abs(self.data[idx2] - img), name='diff2')
            # showImageZoomed(img, name='or', waitkey=False)
            # showMultipleImages([img, self.data[idx2]], waitkey=False)
            # showImageZoomed(self.data[idx], name='c1')
            # showMultipleImages([img, self.data[idx]], waitkey=True, name='c1')
            # showImageZoomed(self.data[idx2], name='c2')
        print(Diffs)
        print()
        return [Diffs[0][0]]

class DistanceClassifier(object):
    def __init__(self):
        self.data = []
        self.classes = []

    def distance(self, point1, point2):
        return sqrt((point1[0] - point1[1]) ** 2 + (point2[0] - point2[1]) ** 2)
    
    def fit(self, X, y):
        assert len(X) == len(y)
        WhitePixels = [np.where(img == 255) for img in X]
        self.data = WhitePixels
        self.classes = y

    def predict(self, img):
        img = img[0]
        PWhitePixels = np.where(img == 255)
        Diffs = []

        for Idx in range(len(self.data)):
            Diff = 0
            for PPIdx in range(len(PWhitePixels[0])):
                for DPIdx in range(len(self.data[Idx][0])):
                    Diff += self.distance((PWhitePixels[0][PPIdx], PWhitePixels[1][PPIdx]), (self.data[Idx][0][DPIdx], self.data[Idx][1][DPIdx]))
            Diffs.append((self.classes[Idx], Diff))
        # print(Diffs)
        Diffs = sorted(Diffs, key=lambda x: x[1])
        # if Diffs[0][0] == 51:
        #     idx = self.classes.index(51)
        #     idx2 = self.classes.index(53)
        #     showImageZoomed(abs(self.data[idx] - img), name='diff1')
        #     showImageZoomed(abs(self.data[idx2] - img), name='diff2')
            # showImageZoomed(img, name='or', waitkey=False)
            # showMultipleImages([img, self.data[idx2]], waitkey=False)
            # showImageZoomed(self.data[idx], name='c1')
            # showMultipleImages([img, self.data[idx]], waitkey=True, name='c1')
            # showImageZoomed(self.data[idx2], name='c2')
        print(Diffs)
        print()
        return [Diffs[0][0]]
        
class HistogramClassifier(object):
    def __init__(self):
        self.cls = SVC(gamma='auto')
    
    def fit(self, X, y):
        assert len(X) == len(y)
        self.histograms = []
        for img in X:
            VHistogram = getHistogramV(img, bins=img.shape[1])
            HHistogram = getHistogramH(img, bins=img.shape[0])
            H = np.concatenate((VHistogram, HHistogram))
            self.histograms.append( H )
        self.classes = y
        self.cls.fit(self.histograms, y)

    def predict(self, imgs):
        PredictedClasses = []
        for img in imgs:
            VHistogram = getHistogramV(img, bins=img.shape[1])
            HHistogram = getHistogramH(img, bins=img.shape[0])
            H = np.concatenate((VHistogram, HHistogram))
            Diffs = []
            for Idx, Histogram in enumerate(self.histograms):
                Diffs.append((self.classes[Idx], sum(abs(H - Histogram))))
            Diffs = sorted(Diffs, key=lambda x: x[1])
            PredictedClasses.append(Diffs[0][0])
        return PredictedClasses

class Classifier(object):
    
    def __init__(self):
        self.initClassifiers()

    def initClassifiers(self):
        X = { 'isolated': [], 'ending': [], 'middle': [], 'beginning': []}
        y = { 'isolated': [], 'ending': [], 'middle': [], 'beginning': []}

        path = 'L/'
        files = []
        for r, d, f in os.walk(path):
            files.extend(f)
            break

        images = []
        for file in files:
            img = loadImage(path + file)
            img = resizeByPadding(img, (50, 50))
            img = cv2.blur(img, ksize=(3, 3))
            # img = cv2.resize(img, (100, 100))
            # img = blackAndWhite(img, thrs=0)
            ClassTuple = eval(file[:file.find('_')])
            ClassIndex = ClassTuple[0] * 25 + ClassTuple[1]
            # _, _, HOGVector = getHOG(img)
            position = 'isolated'
            if ClassTuple[0] == 1: position = 'ending'
            if ClassTuple[0] == 2: position = 'middle'
            if ClassTuple[0] == 3: position = 'beginning'

            X[position].append(img)
            y[position].append(ClassIndex)

        # self.clfs = { 'isolated': SVC(gamma='auto'), 'ending': SVC(gamma='auto'), 'middle': SVC(gamma='auto'), 'beginning': SVC(gamma='auto')}
        self.clfs = { 'isolated': DiffClassifier(), 'ending': DiffClassifier(), 'middle': DiffClassifier(), 'beginning': DiffClassifier()}
        self.clfs2 = { 'isolated': DistanceClassifier(), 'ending': DistanceClassifier(), 'middle': DistanceClassifier(), 'beginning': DistanceClassifier()}
        self.clfs3 = { 'isolated': HistogramClassifier(), 'ending': HistogramClassifier(), 'middle': HistogramClassifier(), 'beginning': HistogramClassifier()}
        for position in self.clfs:
            self.clfs[position].fit(X[position], y[position])
            self.clfs2[position].fit(X[position], y[position])
            self.clfs3[position].fit(X[position], y[position])

    def predict(self, img, position):
        # Gradient, GradientOrientation, HOGVector = getHOG(img)
        img = resizeByPadding(img, (50, 50))
        # img = cv2.resize(img, (100, 100))
        img = cv2.blur(img, ksize=(3, 3))
        # img = blackAndWhite(img, thrs=0)
        PredictedClassIndex = self.clfs[position].predict([img])[0]
        PredictedClassTuple = (PredictedClassIndex // 25, PredictedClassIndex % 25)
        Char = 'S'
        if PredictedClassTuple[0] == 1: Char = 'E'
        if PredictedClassTuple[0] == 2: Char = 'M'
        if PredictedClassTuple[0] == 3: Char = 'B'
        print(Char + str(PredictedClassTuple[1] + 1))
        
        # PredictedClassIndex = self.clfs3[position].predict([img])[0]
        # PredictedClassTuple = (PredictedClassIndex // 25, PredictedClassIndex % 25)
        # Char = 'S'
        # if PredictedClassTuple[0] == 1: Char = 'E'
        # if PredictedClassTuple[0] == 2: Char = 'M'
        # if PredictedClassTuple[0] == 3: Char = 'B'
        # print(Char + str(PredictedClassTuple[1] + 1))
        return PredictedClassTuple