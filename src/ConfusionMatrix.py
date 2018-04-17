import numpy as py
import segmentTag
import operator


def calc_conf_matrix(gold, tagged):
    conf_matrix = {}  # py.zeros([40,40], dtype=int)
    print conf_matrix

    with open(gold) as gold:
        with open(tagged) as tagged:
            for line_gold in gold:
                line_tagged = tagged.readline()
                if line_gold != '\n':
                    gold_word = segmentTag.segmentTag(line_gold.strip())
                    tagged_word = segmentTag.segmentTag(line_tagged.strip())
                    gold_tag = gold_word.tag
                    tagged_tag = tagged_word.tag
                    if gold_tag != tagged_tag:
                        if gold_tag in conf_matrix:

                            if tagged_tag in conf_matrix[gold_tag]:
                                conf_matrix[gold_tag][tagged_tag] += 1
                            else:
                                conf_matrix[gold_tag][tagged_tag] = 1
                        else:
                            conf_matrix[gold_tag] = {}
                            conf_matrix[gold_tag][tagged_tag] = 1

    print conf_matrix
    max_value1 = 1
    max_value2 = 1
    max_value3 = 1
    max_tags1 = ()
    max_tags2 = ()
    max_tags3 = ()
    max_list=[1,1,1]
    max_tag_list=['a','b','c']

    for tag1, tags in conf_matrix.iteritems():
        for tag2, value in tags.iteritems():
            if value > min(max_list):
                min_element_index=max_list.index(min(max_list))
                max_list[min_element_index]=value
                max_tag_list[min_element_index]=(tag1,tag2)

    # print  str(max_value1) + str(max_tags1)
    # print  str(max_value2) + str(max_tags2)
    # print  str(max_value3) + str(max_tags3)
    print max_list
    print max_tag_list


calc_conf_matrix('../heb-pos.gold', '../results/hmm.tagged')
