import train
import decode
import evaluate


def file_len(fname):
    with open(fname) as f:
"""
sad
"""
        for i, l in enumerate(f):
            pass
    return i + 1


def partial_train_and_decode_and_eval():
    file_length = file_len('heb-pos.train')
    print str(file_length)
    tenth = file_length / 10
    print tenth
    for n in range(1, 11, 1):
        print n
        with open("heb-pos.train") as train_file:
            head = [next(train_file) for x in xrange(tenth * n)]
        with open("exps/partial.train", "w+") as partial:
            for line in head:
                partial.write(line)
        train.run('2', "exps/partial.train", 'y')
        decode.run('2','heb-pos.test', 'exps/hmm-part-smooth-y.lex', 'exps/hmm-part-smooth-y.gram')
        evaluate.run('results/hmm.tagged','heb-pos.gold','2','y')


partial_train_and_decode_and_eval()
