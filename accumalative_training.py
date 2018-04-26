import train
import decode
import evaluate


def file_len(fname):
    with open(fname) as f:
###
This should get a path rather than a name, as what if the the file isn't in the same path as the executable (main).
That way this general function will be general
###
        for i, l in enumerate(f):
            pass
    return i + 1


def partial_train_and_decode_and_eval():
###
Just "partial_train_decode_eval"  :)
###
    file_length = file_len('heb-pos.train')
    print str(file_length)
###
No need for "str" when using print, it already enables str to the screen output.
Some explanation prints before the numbers so we (and you) can understand what's printed
###
    tenth = file_length / 10
    print tenth
    for n in range(1, 11, 1):
###
range default step is 1 (the 3rd parameter).
What are 1, 11 ? These numbers should be const variables with a meaningful name
###
        print n
        with open("heb-pos.train") as train_file:
            head = [next(train_file) for x in xrange(tenth * n)]
###
Why here you use xrange and before range?
Will head contain all the first lines in the tenths file parts? I think it will contain the "tenth" first lines
###
        with open("exps/partial.train", "w+") as partial:
            for line in head:
                partial.write(line)
        train.run('2', "exps/partial.train", 'y')
        decode.run('2','heb-pos.test', 'exps/hmm-part-smooth-y.lex', 'exps/hmm-part-smooth-y.gram')
        evaluate.run('results/hmm.tagged','heb-pos.gold','2','y')


partial_train_and_decode_and_eval()
###
What is this random application of "partial_train_and_decode_and_eval"?
###
