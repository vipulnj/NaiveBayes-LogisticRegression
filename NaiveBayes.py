import sys
import os.path
import codecs
import re
import math

if __name__ == '__main__':
    hamTrSet = sys.argv[1]
    spamTrSet = sys.argv[2]
    hamTestSet = sys.argv[3]
    spamTestSet = sys.argv[4]
    shouldRemoveStopwords = sys.argv[5]      # whether to use stop words or not

    hamWordsDict = {}       # dictionary to store ham words and their count in ham mails
    spamWordsDict = {}      # dictionary to store spam words and their count in spam mails

    # read stopwords in stopwords.txt enclosed
    stopwordsFile = "stopwords.txt"
    stopwordsList = []
    if shouldRemoveStopwords == "y":
        with open(stopwordsFile) as f:
            stopwordsList = f.read().split()

    fcountSpamTr = fcountHamTr = 0      # count of ham and spam training files

    for root, dirs, files in os.walk(hamTrSet):
        for file in files:
            if not file.startswith("."):
                fcountHamTr += 1
                with codecs.open(hamTrSet + '/' + file, "r", 'ISO-8859-1', errors='ignore') as f:       # ignore accented characters
                    hamWords = f.read().lower().split()
                    hamWords = [hamWord for hamWord in hamWords if re.match(r'[a-zA-Z]', hamWord)]
                    hamWords = [hamWord for hamWord in hamWords if hamWord not in stopwordsList]
                    for aWord in hamWords:
                        if aWord not in hamWordsDict:
                            hamWordsDict[aWord] = 1
                        if aWord in hamWordsDict:
                            count = hamWordsDict[aWord]
                            count += 1
                            hamWordsDict[aWord] = count

    for root, dirs, files in os.walk(spamTrSet):
        for file in files:
            if not file.startswith("."):
                fcountSpamTr += 1
                with codecs.open(spamTrSet + '/' + file, "r", 'ISO-8859-1', errors='ignore') as f:       # ignore accented characters
                    spamWords = f.read().lower().split()
                    spamWords = [spamWord for spamWord in spamWords if re.match(r'[a-zA-Z]', spamWord)]
                    spamWords = [spamWord for spamWord in spamWords if spamWord not in stopwordsList]
                    for aWord in spamWords:
                        if aWord not in spamWordsDict:
                            spamWordsDict[aWord] = 1
                        if aWord in spamWordsDict:
                            count = spamWordsDict[aWord]
                            count += 1
                            spamWordsDict[aWord] = count

    # add to get total number of files
    totalCountTr = fcountHamTr + fcountSpamTr
    # calculate prior probability
    priorProbHam = float(fcountHamTr) / float(totalCountTr)
    priorProbSpam = float(fcountSpamTr) / float(totalCountTr)

    countOfAllHamWords = 0
    for key in hamWordsDict.keys():
        countOfWord = hamWordsDict.get(key)
        countOfAllHamWords += countOfWord
    # what comes in denominator for laplace smoothing - adding the number of values observed for ham
    deno_condProb_Ham = countOfAllHamWords + len(hamWordsDict) + len(spamWordsDict)

    countOfAllSpamWords = 0
    for key in spamWordsDict.keys():
        countOfWord = spamWordsDict.get(key)
        countOfAllSpamWords += countOfWord
    # what comes in denominator for laplace smoothing - adding the number of values observed for spam
    deno_condProb_Spam = countOfAllSpamWords + len(spamWordsDict) + len(hamWordsDict)

    # take words exclusive to each lists and add it to other dictionary with size 0
    hamWordsList = set(hamWordsDict.keys())
    spamWordsList = set(spamWordsDict.keys())
    wordsInSpamListOnly = list(set(spamWordsList) - set(hamWordsList))
    wordsInHamListOnly = list(set(hamWordsList) - set(spamWordsList))

    for word in wordsInSpamListOnly:
        hamWordsDict[word] = 0

    for word in wordsInHamListOnly:
        spamWordsDict[word] = 0

    hamWordsDict_prob = {}
    spamWordsDict_prob = {}

    # calculate condtional probabilities for each word in the two dictionaries
    for word in hamWordsDict:
        try:
            countOfWord = hamWordsDict[word]
        except KeyError:
            countOfWord = 0
        condProb_Ham = (countOfWord + 1) / float(deno_condProb_Ham)     # laplace smoothing
        hamWordsDict_prob[word] = condProb_Ham

    for word in spamWordsDict:
        try:
            countOfWord = spamWordsDict[word]
        except KeyError:
            countOfWord = 0
        condProb_Spam = (countOfWord + 1) / float(deno_condProb_Spam)   # laplace smoothing
        spamWordsDict_prob[word] = condProb_Spam

    ''' classifying test data '''
    hamClassifiedCount = spamClassifiedCount = 0
    fCount = 0
    correctClassification = wrongClassification = 0

    testSet = [hamTestSet, spamTestSet]
    for ts in testSet:
        for root, dirs, files in os.walk(ts):
            for file in files:
                if not file.startswith('.'):        # ignore system files
                    fCount += 1                     # count number of files
                    with codecs.open(ts + '/' + file, "r", 'ISO-8859-1', errors='ignore') as f:
                        words = f.read().lower().split()
                        words = [word for word in words if re.match(r'[a-zA-Z]', word)]

                        scoreHam = math.log10(priorProbHam)
                        scoreSpam = math.log10(priorProbSpam)

                        for word in words:
                            try:
                                scoreHam += math.log10(hamWordsDict_prob[word])
                                scoreSpam += math.log10(spamWordsDict_prob[word])
                            except KeyError:
                                pass

                        hamClassifiedCount += 1 if scoreHam > scoreSpam else 0
                        spamClassifiedCount += 1 if scoreSpam > scoreHam else 0

                        if scoreHam > scoreSpam:
                            correctClassification += 1 if ts == hamTestSet else 0
                            wrongClassification += 0 if ts == spamTestSet else 0

                        if scoreHam < scoreSpam:
                            correctClassification += 1 if ts == spamTestSet else 0
                            wrongClassification += 1 if ts == hamTestSet else 0

    print ("Correct Classification = ", (correctClassification/float(fCount)) * 100 , "%")