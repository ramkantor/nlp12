import math
from segmentTag import segmentTag

# Calculating word accuracy and sentence in one loop

def calcWordSentenceAcc(taggedFile, goldFile):
    calc = {}
    sentence = 0
    sentenceLength = 0
    hitCount = 0
    with open(taggedFile) as tagged:
        with open(goldFile) as gold:

            for line in tagged:

                if line == '\n':
                    if sentenceLength == 0:
                        pass
                    else:
                        goldLine = gold.readline()
                        rate = hitCount / sentenceLength
                        calc[sentence] = (sentenceLength, hitCount, math.floor(rate))
                        sentenceLength = 0
                        hitCount = 0
                        sentence += 1

                else:
                    sentenceLength += 1
                    goldLine = gold.readline()
                    try:
                        tagGold = segmentTag(goldLine).tag
                    except:
                        print goldLine
                    try:
                        tag = segmentTag(line).tag
                    except:
                        print line
                    if tag == tagGold:
                        hitCount += 1
        print calc
    All_jSum = 0
    hitSum = 0
    sumOfSentences = 0
    for key, value in calc.iteritems():
        All_jSum += value[2]
        hitSum += value[1]
        sumOfSentences += value[0]

    all = All_jSum / len(calc)
    A = float(hitSum) / float(sumOfSentences)
    print 'All: ', all, 'A: ', A