import operator

import accuracy
from segmentTag import segmentTag


class BasicTagger:
"""
WHY SO MUCH SPACEEEEE
"""



    def training(self, file_):
        dic = {}
"""
"dic" is ambiguous (and rude ;))
"""
        tags = {}
        mostCommonTag = {}

        with open(file_) as hebPos:
            for line in hebPos:
                if line != '\n':
                    seg = segmentTag(line)
                    if seg.segment in dic:
                        if seg.tag in dic[seg.segment]:
                            dic[seg.segment][seg.tag] += 1
                        else:
                            dic[seg.segment][seg.tag] = 1
                    else:
                        dic[seg.segment] = {seg.tag: 1}
"""
This line can be instead of lines 26 - 32:
dic[seg.segment].update({seg.tag: dic[seg.segment].get(seg.tag, 0) + 1}) if seg.segment in dic else dic.update({seg.segment: {seg.tag: 1}})  
"""
            for seg in dic:
                mostCommonTag[seg] = max(dic[seg].iteritems(), key=operator.itemgetter(1))[0]
        with open('exps/basic.lex', 'w+') as lex:
            for seg, value in mostCommonTag.iteritems():
                lex.write(seg + '\t' + value + '\n')

    def tag(self, test_file,param_file):
        mostCommonTag={}
        with open(param_file) as lex:
            for line in lex:
                tup=line.split()
                mostCommonTag[tup[0]]=tup[1]
        tagged = ""
        with open(test_file) as hebPos:
            for line in hebPos:
                if line != '\n':
                    if mostCommonTag.has_key(line.strip()):
                        tagged += line.strip() + '\t' + mostCommonTag[line.strip()] + '\n'
                    else:
                        tagged += line.strip() + '\t' + 'NNP\n'
                else:
                    tagged += "\n"

        with open('results/basic.tagged', 'w+') as taggedFile:
            taggedFile.write(tagged)


def train(file, smoothing):
    basicTagger_ = BasicTagger()
    basicTagger_.training('heb-pos.train')
    print 'finished basic parser training'


def decode(test_file, param_file_1, param_file_2):
    basicTagger_ = BasicTagger()
    basicTagger_.tag(test_file,param_file_1)
    print 'finished basic tagger decoding'



#decode('../heb-pos.test','../exps/basic.lex',None)
#
# accuracy.calcWordSentenceAcc('results/basic.tagged', 'exps/heb-pos.gold','basic','baseline','NO')
