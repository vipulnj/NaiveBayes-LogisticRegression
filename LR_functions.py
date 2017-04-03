import math
w0 = float(-1)


def calculateProb(wordDict, weights):
    sigma_WtimesX = 0
    for word in wordDict:
        occurences = wordDict[word]
        try:
            weight = float(weights[word])
        except KeyError:
            pass
        sigma_WtimesX += float(occurences * weight)
    prob = sigmoid(sigma_WtimesX)
    return prob


def sigmoid(sigma_WtimesX):
    if sigma_WtimesX > 500:
        val = float(1.0)
    elif sigma_WtimesX < -500:
        val = float(0.0)
    elif -500 < sigma_WtimesX < 500:
        val = float(1 / float((1 + math.exp(-1 * (w0 + sigma_WtimesX)))))
    return val


def sumArray(words, weights):
    result_WtimesX = 0
    for word in words:
        try:
            result_WtimesX += weights[word]
        except KeyError:
            pass
    return result_WtimesX