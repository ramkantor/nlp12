import re


def calc_num_of_unigrams(file):
    non_blank_count = 0
    with open(file) as gold:
        for line in gold:
            if line.strip():
                non_blank_count += 1
        print ('unigram instances', non_blank_count)

def num_of_unigram_types(file):
    num_of_types = 0
    lst = []
    with open(file) as gold:
        for line in gold:
            if line != '\n':
                # print line
                unigram = re.split(r'\t', line)
                # print unigram[0] segment
                if unigram[0] in lst:
                    pass
                else:
                    ++num_of_types
                    lst.append(unigram[0])
        print ('types of unigram', len(lst))

def num_of_segments_types(file):
    num_of_types = 0
    lst = []
    with open(file) as gold:
        for line in gold:
            if line != '\n':
                if line in lst:
                    pass
                else:
                    ++num_of_types
                    lst.append(line)
        print ('types of segment tags', len(lst))

print "gold"

calc_num_of_unigrams('../heb-pos.gold')
num_of_unigram_types('../heb-pos.gold')
num_of_segments_types('../heb-pos.gold')

print "train"
calc_num_of_unigrams('../heb-pos.train')
num_of_unigram_types('../heb-pos.train')
num_of_segments_types('../heb-pos.train')
