import sys
import os.path
import codecs
import re
import LR_functions as func

if __name__ == '__main__':
    hamTrSet = sys.argv[1]
    spamTrSet = sys.argv[2]
    hamTestSet = sys.argv[3]
    spamTestSet = sys.argv[4]
    shouldRemoveStopwords = sys.argv[5]
    numOfIterations = int(sys.argv[6])
    learningRate = float(sys.argv[7])
    shouldRegularizeParams = sys.argv[8]
    try:
        lambdaVal = float(sys.argv[9])
    except IndexError:
        if shouldRegularizeParams == "y":
            print "Lambda value missing.. "
            exit(0)

    wordsDict = {}

    stopwordsFile = "stopwords.txt"
    stopwordsList = []
    if shouldRemoveStopwords == "y":
        with open(stopwordsFile) as f:
            stopwordsList = f.read().split()

    # all words' count in both ham and spam mail documents
    trainingSets = [hamTrSet, spamTrSet]
    for trSet in trainingSets:
        for root, dirs, files in os.walk(trSet):
            for file in files:
                with codecs.open(trSet + '/' + file, "r", 'ISO-8859-1', errors='ignore') as f:  # ignore accented characters
                    words = f.read().lower().split()
                    words = [word for word in words if re.match(r'[a-zA-Z]', word)]  # alphabets only
                    words = [word for word in words if word not in stopwordsList]
                    for word in words:
                        if word not in wordsDict:
                            wordsDict[word] = float(1)
                        if word in wordsDict:
                            count = float(wordsDict[word])
                            count += float(1)
                            wordsDict[word] = float(count)

    # dictionary which will contain the weight of each word. Assign all a weight of 1 initially
    weights = {}
    for key in list(wordsDict.keys()):
        weights[key] = float(1)

    # dictionary of word count in each mail document
    mail_wordcountDict = {}
    trainingSets = [hamTrSet, spamTrSet]
    for trSet in trainingSets:
        for root, dirs, files in os.walk(trSet):
            for file in files:
                if not file.startswith('.'):        # ignore hidden files related to system
                    with codecs.open(trSet + '/' + file, "r", 'ISO-8859-1', errors='ignore') as f:
                        wordsInMail = f.read().split()
                        wordsInMail = [word for word in wordsInMail if re.match(r'[a-zA-Z]', word)]  # keeping only alphanumeric text
                        wordsInMail = [word for word in wordsInMail if word not in stopwordsList] # remove stopwords. If we do not want to, stopwords in an empty list

                        wordsInMailDict = {}
                        for word in wordsInMail:
                            if word not in wordsInMailDict:
                                wordsInMailDict[word] = 1
                            elif word in wordsInMailDict:
                                count = wordsInMailDict[word]
                                count += 1
                                wordsInMailDict[word] = count

                        mail_wordcountDict[file] = wordsInMailDict      # LHS gives a dict of word count in each file

    if shouldRegularizeParams == "y":
        print "Parameters to be regularized.. "

    # training to set weights of words
    for i in range(0, numOfIterations):
        trainingSets = [hamTrSet, spamTrSet]
        for trSet in trainingSets:
            for root, dirs, files in os.walk(trSet):
                for file in files:
                    if not file.startswith("."):
                        weightError = 0

                        if trSet == hamTrSet:
                            classOfMail = 1
                        if trSet == spamTrSet:
                            classOfMail = 0

                        wordsInMailDict = mail_wordcountDict[file]
                        prob = func.calculateProb(wordsInMailDict, weights)
                        error = float((classOfMail - prob))

                        for word in wordsInMailDict:
                            try:
                                weightError += float(wordsInMailDict[word] * error)
                            except KeyError:
                                weightError = 0
                            try:
                                wt = weights[word]
                            except KeyError:
                                pass

                            if shouldRegularizeParams == "y":
                                newWeight = float(wt + float(float(learningRate) * float(weightError))) - float(learningRate * lambdaVal * wt)
                            else:
                                newWeight = float(wt + float(float(learningRate) * float(weightError)))
                            weights[word]= float(newWeight)

    # testing classification
    correctClassification = wrongClassification = 0
    testFileCount = 0

    testSets = [hamTestSet, spamTestSet]
    for ts in testSets:
        for root, dirs, files in os.walk(ts):
            for file in files:
                if not file.startswith("."):
                    testFileCount += 1
                    with codecs.open(ts + '/' + file, "r", 'ISO-8859-1', errors='ignore') as f:  # ignore accented characters
                        words = f.read().split()
                        words = [word for word in words if re.match(r'[a-zA-Z]', word)]  # alphabets only
                        words = [word for word in words if word not in stopwordsList]

                        weightedSum = func.sumArray(words, weights)
                        hamProb = func.sigmoid(weightedSum)
                        spamProb = 1 - hamProb

                    if spamProb > hamProb:
                        if ts == spamTestSet:
                            correctClassification += 1
                        else:
                            wrongClassification += 1
                    else:
                        if ts == hamTestSet:
                            correctClassification += 1
                        else:
                            wrongClassification += 1

    print "Correct Classification = ", float(correctClassification/float(testFileCount)) * 100, "%"