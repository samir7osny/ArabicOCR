import numpy as np
from sklearn import linear_model
from sklearn.datasets import make_classification
from math import log, exp
X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1], [-2, 1], [3, 1], [2, 3], [1, -1], [5, 1]])
Y = np.array([1, 1, 2, 2, 1, 3, 4, 4, 5])
# clf = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
# clf.fit(X, Y)

X, Y = make_classification(n_samples=100, n_features=50, n_informative=5, n_classes=5, n_redundant=0, random_state=0, shuffle=True)
# print(X[50])
# exit()

Classifiers = []
WClassifiers = []

NClass = 106
NClassifier = 10

W = np.zeros(len(X))
W[:] = 1 / len(W)

def pi(ym, xm, classifier):
    return (0 if ym == classifier.predict([xm])[0] else 1)

def computeError(w, x, y, classifier):
    wsum = sum(w)
    return sum([(w[Index] * pi(y[Index], x[Index], classifier)) / wsum for Index in range(len(w))])

def predict(wclassifiers, classifiers, x):
    Result = np.zeros(5)
    for c in range(NClassifier):
        for cl in range(5):
            Result[cl] += wclassifiers[c] * (1 - pi(cl, x, classifiers[c]))

    return Result

for t in range(NClassifier):
    Classifier = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
    Classifier.fit(X, Y)

    Classifiers.append(Classifier)

    Error = computeError(W, X, Y, Classifier)
    WClassifier = log((1 - Error) / Error) if Error != 0 else 999
    WClassifiers.append(WClassifier)

    W = [W[Index] * exp(WClassifier * pi(Y[Index], X[Index], Classifier)) for Index in range(len(W))]

    WSum = sum(W)
    W = [W[Index] / WSum for Index in range(len(W))]

# print(WClassifiers)
RandomIndex = np.random.choice(range(100))
print(RandomIndex)
print(predict(WClassifiers, Classifiers, X[RandomIndex]))
print(Y[RandomIndex])

# [ 2.0544041, -0.70742659, -1.07605657, -0.86864918, -0.87916349, -0.11496177,  0.49585067, -1.32052535,  0.49908428,  0.3062034, 0.36369789, 0.31263396, -0.19346388, 1.24129922, -0.15589799, -0.7391692, -0.05872619, -0.95051795, -0.46399642, -0.17724662, -0.37955412,  0.19939707, 1.94576139, 0.57094984, 1.07230065, -0.50370944, -0.58701629, -0.37817805,  0.8528891, -2.14811848, -1.03316478, 0.10233585, -0.22409237, 1.96772968, 0.44768322, -0.66219144, -1.57760707, -0.34056003, -1.30322008, 0.46675065, 0.16110632, 0.32003193, 2.07917666, -0.90746598, -0.19240421, -1.21251574, -0.08059852, 1.59327362, 0.5687224, -0.11448705]