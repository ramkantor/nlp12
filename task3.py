import math
import collections
import viterbi
import itertools
import accuracy
import segmentTag


class HMM_tagger:
    def createLexicalFile(self, trainFile, smoothing):
        dicSeg = {}
        dicTag = {}
        with open(trainFile)as train:
            for line in train:
                if line != '\n':
                    tuple = segmentTag.segmentTag(line)
                    if tuple.tag in dicTag:
                        dicTag[tuple.tag] += 1
                    else:
                        dicTag[tuple.tag] = 1
                    if dicSeg.has_key(tuple.segment):
                        if dicSeg[tuple.segment].has_key(tuple.tag):
                            dicSeg[tuple.segment][tuple.tag] += 1
                        else:
                            dicSeg[tuple.segment][tuple.tag] = 1
                    else:
                        dicSeg[tuple.segment] = {}
                        dicSeg[tuple.segment][tuple.tag] = 1
            if smoothing:
                removeList = []
                dicSeg['UNK'] = {}
                for seg, dic in dicSeg.iteritems():
                    if sum(dic.values()) == 1:
                        for tag, val in dic.iteritems():
                            if tag in dicSeg['UNK']:
                                dicSeg['UNK'][tag] += 1
                            else:
                                dicSeg['UNK'][tag] = 1
                        removeList.append(seg)
                for x in removeList:
                    del dicSeg[x]

        with open('files/heb-pos.lex', 'w+') as lex:

            for key, value in dicSeg.iteritems():
                lex.write(key + '\t')
                for key_2, value_2 in value.iteritems():
                    lex.write(key_2 + '\t' + "%.9f" % math.log(float(value_2) / dicTag[key_2]) + '\t')

                lex.write('\n')
            if not smoothing:
                lex.write('UNK' + '\t' + 'NNP' + '\t' + "%.9f" % math.log(1) + '\t')

    def createTagLists(self, trainFile):
        listOflists = []
        list = []
        with open(trainFile)as train:
            for line in train:
                if line != '\n':
                    tag = segmentTag.segmentTag(line).tag
                    list.append(tag)
                else:
                    listOflists.append(list)
                    list = []
        # print  listOflists
        return listOflists

    def createTransitionFile(self, trainFile, smoothing):
        tagSentences = self.createTagLists(trainFile)

        # unigram probs
        unigrams = self.conditionGramCount(tagSentences, 1)
        num_of_unigrams_type = len([item for sublist in unigrams for item in sublist])

        dicTag = {}
        with open(trainFile)as train:
            for line in train:
                if line != '\n':
                    tuple = segmentTag.segmentTag(line)
                    if tuple.tag in dicTag:
                        dicTag[tuple.tag] += 1
                    else:
                        dicTag[tuple.tag] = 1
        Num_of_Tags = sum(dicTag.values())
        bigrams = self.ngramCounter(tagSentences, 2)

        bigramProb = self.ngramProb(unigrams, bigrams, 2, dicTag, smoothing)
        Delta = 0.00001
        with open('files/heb-pos.gram', 'w+') as gram:
            gram.write("\n\\1-grams\\\n")
            for key, value in dicTag.iteritems():
                gram.write("%.9f" % math.log(float(value) / Num_of_Tags) + '\t' + key + '\n')
            gram.write("\n\\2-grams\\\n")
            if not smoothing:
                for key, value in bigramProb.iteritems():
                    gram.write("%.9f" % math.log(value) + '\t' + '\t'.join(str(x) for x in key) + '\n')
            else:
                dicTag['<s>'] = 1
                dicTag['<e>'] = 1

                for pos1 in dicTag:
                    for pos2 in dicTag:
                        if (pos1, pos2) not in bigramProb:
                            gram.write("%.9f" % math.log(float(Delta) / (Delta * Num_of_Tags)) + '\t' + '\t'.join(
                                str(x) for x in (pos1, pos2)) + '\n')
                        else:
                            gram.write("%.9f" % math.log(float(bigramProb[(pos1, pos2)])) + '\t' + '\t'.join(
                                str(x) for x in (pos1, pos2)) + '\n')


                            # bigramsProbs=probNgram(unigrams,bigra)

    def ngramProb(self, conditionGram, nGram, n, dicTag, smoothing):
        conditionGram = dict(conditionGram)
        prob = {}
        Delta = 0.00001
        for line in nGram:
            condition = line[0][:n - 1]
            count = conditionGram[condition]
            if smoothing:
                prob[line[0]] = (float(line[1]) + Delta) / (count + Delta * len(conditionGram))
            else:
                prob[line[0]] = float(line[1]) / count

        # print prob
        return prob

    def ngramCounter(self, tagSentences, n):
        lst = []
        for sentence in tagSentences:
            sentence = (n - 1) * ['<s>'] + sentence + (n - 1) * ['<e>']
            lst += zip(*[sentence[i:] for i in range(n)])
        lst = collections.Counter(lst).most_common()
        return lst

    def conditionGramCount(self, tagSentences, n):
        lst = []
        for sentence in tagSentences:
            sentence = n * ['<s>'] + sentence + n * ['<e>']
            lst += zip(*[sentence[i:] for i in range(n)])
        lst = collections.Counter(lst).most_common()

        return lst


hmm = HMM_tagger()
hmm.createLexicalFile('files/heb-pos.train', True)
hmm.createTransitionFile('files/heb-pos.train', False)

if __name__ == "__main__":
    start_p = {}
    trans_p = {}
    states = []
    emit_p = {}
    end_p = {}
    lines = open('files/heb-pos.gram').read().split('\n\n')
    lines = lines[1].split('\n')
    print lines
    for line in lines:

        if line.strip() != '\\2-grams\\' and line != '':
            splited = line.strip().split('\t')
            prob = splited[0]
            pos1 = splited[1]
            pos2 = splited[2]
            if pos1 not in states:
                states.append(pos1)
            if pos2 not in states:
                states.append(pos2)
            if (pos1 == '<s>'):
                start_p[pos2] = float(prob)
            if (pos2 == '<e>'):
                end_p[pos1] = float(prob)
            else:
                if pos1 in trans_p:
                    trans_p[pos1].update({pos2: float(prob)})
                else:
                    trans_p[pos1] = {pos2: float(prob)}

    with open('files/heb-pos.lex') as lex:
        corpus = []
        for line in lex:
            splited = line.strip().split('\t')
            seg = splited[0]
            sliced = splited[1:]
            if seg not in corpus:
                corpus.append(seg)

            for state in zip(sliced[0::2], sliced[1::2]):
                if state[0] in emit_p:
                    emit_p[state[0]].update({seg: float(state[1])})
                else:
                    emit_p[state[0]] = {seg: float(state[1])}

    # obs = ['EFRWT', 'ANFIM', 'MGIEIM', 'M', 'TAILND', 'L', 'IFRAL', 'KF', 'HM', 'NRFMIM', 'K', 'MTNDBIM', 'yyCM', 'AK',
    #        'LMEFH', 'MFMFIM', 'EWBDIM', 'FKIRIM', 'ZWLIM', 'yyDOT']

    with open('files/heb-pos.test') as test:
        lines = test.readlines()

        sentences = [list(x[1]) for x in
                     itertools.groupby(lines, lambda x: x == '\n')
                     if not x[0]]

    states.remove('<s>')
    states.remove('<e>')

    tagged = []

    for idx, obs in enumerate(sentences):
        obs = (map(lambda x: x.strip(), obs))
        tagged.append(viterbi.viterbi(obs, states, start_p, trans_p, emit_p, end_p, corpus))
        print 'tagged sentence num ', idx

    with open('files/viterbi.tagged', 'w+') as tagfile:
        for line in tagged:
            for word in line:
                seg, pos = word
                tagfile.write(seg + '\t' + pos + '\n')
            tagfile.write('\n')
accuracy.calcWordSentenceAcc('files/viterbi.tagged', 'files/heb-pos.gold')
