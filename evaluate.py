import sys
import src.accuracy


def run(tagged_file, gold_file, model, smoothing):
    print model
    names = {'1': 'basic-', '2': 'hmm-smoothing-'}
    src.accuracy.eval(tagged_file, gold_file, model, smoothing, names[model] + smoothing)


if __name__ == "__main__":
    tagged_file = sys.argv[1]
    gold_file = sys.argv[2]
    model = sys.argv[3]
    smoothing = sys.argv[4]
    run(tagged_file, gold_file, model, smoothing)
