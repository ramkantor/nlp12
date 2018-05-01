import itertools
import viterbi


def preprocess_and_run_viterbi(test_file,param_file_1,param_file_2):
    global line, seg, tagged
"""
Usually try to avoid using global params
"""
    start_p = {}
    trans_p = {}
    states = []
    emit_p = {}
    end_p = {}
"""
Can also be: start_p, trans_p = {}, {}
"""
    lines = open(param_file_2).read().split('\n\n')
    lines = lines[1].split('\n')
"""
lines = open(param_file_2).read().split('\n\n')[1].split('\n')
"""

    for line in lines:

        if line.strip() != '\\2-grams\\' and line != '':
"""
The first rule of "line.strip() != '\\2-grams\\'" is enough
"""
            splited = line.strip().split('\t')
            prob = splited[0]
            pos1 = splited[1]
            pos2 = splited[2]
"""
prob, pos1, pos2 = splited[0], splited[1], splited[2]
"""
            if pos1 not in states:
                states.append(pos1)
"""
states.append(pos1) if pos1 not in states else None
"""
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
"""
trans_p[pos1].update({pos2: float(prob)}) if pos1 in trans_p else trans_p[pos1].update({pos2: float(prob)})
"""
    with open(param_file_1) as lex:
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
    with open(test_file) as test:
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



    with open('results/hmm.tagged', 'w+') as tagfile:
        for line in tagged:
            for word in line:
                seg, pos = word
                tagfile.write(seg + '\t' + pos + '\n')
            tagfile.write('\n')


def decode(test_file, param_file_1, param_file_2):
    preprocess_and_run_viterbi(test_file, param_file_1, param_file_2)
    print 'finished hmm tagger decoding'
    print 'output: results/hmm.tagged '
