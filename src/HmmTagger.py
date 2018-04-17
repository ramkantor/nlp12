import collections
import math

import segmentTag

""" This class is responsible for training the tagger and create output file
 such as *.gram and *.lex """


class HMMTagger:
    """@params: train file, smoothing-True/False
        return empty
        creates a *.lex file"""

    def create_lexical_file(self, trainFile, smoothing):
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

                        # SMOOTHING HANDLING
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

        # .lex file writing
        if smoothing:
            sm='y'
        else:
            sm='n'
        with open('exps/hmm-smooth-'+sm+'.lex', 'w+') as lex:

            for key, value in dicSeg.iteritems():
                lex.write(key + '\t')
                for key_2, value_2 in value.iteritems():
                    lex.write(key_2 + '\t' + "%.9f" % math.log(float(value_2) / dicTag[key_2]) + '\t')

                lex.write('\n')
            if not smoothing:
                lex.write('UNK' + '\t' + 'NNP' + '\t' + "%.9f" % math.log(1) + '\t')

    def create_tag_lists(self, trainFile):
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

    """@params: train file, smoothing-True/False
        return empty
        creates a *.gram file"""

    def create_transition_file(self, trainFile, smoothing):
        tagSentences = self.create_tag_lists(trainFile)

        # unigram probs
        unigrams = self.condition_gram_count(tagSentences, 1)

        bigrams = self.ngram_counter(tagSentences, 2)
        bigramProb = self.calc_ngram_transition_prob(unigrams, bigrams, 2, smoothing)
        Delta = 0.00001

        dic_tag = {}
        with open(trainFile)as train:
            for line in train:
                if line != '\n':
                    tuple = segmentTag.segmentTag(line)
                    if tuple.tag in dic_tag:
                        dic_tag[tuple.tag] += 1
                    else:
                        dic_tag[tuple.tag] = 1

        num_of_tags = sum(dic_tag.values())


        if smoothing:
            sm = 'y'
        else:
            sm = 'n'
        with open('exps/hmm-smooth-'+sm+'.gram', 'w+') as gram:
            gram.write("\n\\1-grams\\\n")
            for key, value in dic_tag.iteritems():
                gram.write("%.9f" % math.log(float(value) / num_of_tags) + '\t' + key + '\n')
            gram.write("\n\\2-grams\\\n")
            if not smoothing:
                for key, value in bigramProb.iteritems():
                    gram.write("%.9f" % math.log(value) + '\t' + '\t'.join(str(x) for x in key) + '\n')
            else:
                dic_tag['<s>'] = 1
                dic_tag['<e>'] = 1

                for pos1 in dic_tag:
                    for pos2 in dic_tag:
                        if (pos1, pos2) not in bigramProb:
                            gram.write("%.9f" % math.log(float(Delta) / (Delta * num_of_tags)) + '\t' + '\t'.join(
                                str(x) for x in (pos1, pos2)) + '\n')
                        else:
                            gram.write("%.9f" % math.log(float(bigramProb[(pos1, pos2)])) + '\t' + '\t'.join(
                                str(x) for x in (pos1, pos2)) + '\n')

    def calc_ngram_transition_prob(self, conditionGram, nGram, n, smoothing):
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

        return prob

    """This method count the bigram instance -ngram count(w_i,w_i-w)"""

    def ngram_counter(self, tagSentences, n):
        lst = []
        for sentence in tagSentences:
            sentence = (n - 1) * ['<s>'] + sentence + (n - 1) * ['<e>']
            lst += zip(*[sentence[i:] for i in range(n)])
        lst = collections.Counter(lst).most_common()
        return lst

    """This method count the unigram instance ngram count(w_i)"""

    def condition_gram_count(self, tagSentences, n):
        lst = []
        for sentence in tagSentences:
            sentence = n * ['<s>'] + sentence + n * ['<e>']
            lst += zip(*[sentence[i:] for i in range(n)])
        lst = collections.Counter(lst).most_common()

        return lst

def train(file,smoothing):
    hmm = HMMTagger()
    hmm.create_lexical_file(file, smoothing)
    hmm.create_transition_file(file, smoothing)
