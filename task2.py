import numpy as py

import operator
import math
import accuracy
from segmentTag import segmentTag





class basicTagger:
    def __init__(self):
        self.mostCommonTag = {}

    def training(self, file_):
        dic = {}
        tags = {}

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
            for seg in dic:
                self.mostCommonTag[seg] = max(dic[seg].iteritems(), key=operator.itemgetter(1))[0]
        print self.mostCommonTag

    def tag(self, file_):
        tagged = ""
        with open(file_) as hebPos:
            for line in hebPos:
                if line != '\n':
                    if self.mostCommonTag.has_key(line.strip()):
                        tagged += line.strip() + '\t' + self.mostCommonTag[line.strip()] + '\n'
                    else:
                        tagged += line.strip() + '\t' + 'NNP\n'
                else:
                    tagged += "\n"
        print tagged
        try:
            with open('files/basic.tagged') as taggedFile:
                taggedFile.write(tagged)
        except IOError:
            with open('files/basic.tagged', 'w+') as taggedFile:
                taggedFile.write(tagged)




basicTagger_ = basicTagger()
basicTagger_.training('files/heb-pos.train')
basicTagger_.tag('files/heb-pos.test')
accuracy.calcWordSentenceAcc('files/basic.tagged', 'files/heb-pos.gold')
