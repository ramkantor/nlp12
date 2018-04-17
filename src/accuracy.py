import math
from segmentTag import segmentTag


# Calculating word accuracy and sentence in one loop

def calcWordSentenceAcc(taggedFile, goldFile, file_name, model, smoothing):
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
        #print calc
    All_jSum = 0
    hitSum = 0
    sumOfSentences = 0
    with open('results/' + file_name + '.eval', 'w+') as eval:
        eval.write("# Model:\t" + model + '\n')
        eval.write("# Smoothing:\t" + smoothing + '\n')
        eval.write("# Test File:\t" + 'exps\heb-pos.test' + '\n')
        eval.write("# Gold File:\t" + 'exps\heb-pos.gold' + '\n\n')
        line_num = 0
        for key, value in calc.iteritems():
            line_num += 1
            sentence_acc = value[2]
            sentence_hit_sum = value[1]
            sentence_length = value[0]
            eval.write(str(line_num) + '\t' + str((float(sentence_hit_sum) / sentence_length)) + '\t' + str(
                sentence_acc) + '\n')

            All_jSum += sentence_acc
            hitSum += sentence_hit_sum
            sumOfSentences += sentence_length

        all = All_jSum / len(calc)
        A = float(hitSum) / float(sumOfSentences)
        eval.write('macro-avg' + '\t' + str(A) + '\t' + str(all))
    print 'All: ', all, 'A: ', A


def eval(tagged_file, gold_file, model, smoothing, file_name):
    calcWordSentenceAcc(tagged_file, gold_file, file_name, model, smoothing)
    print 'finished basic tagger decoding'
