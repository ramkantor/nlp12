import sys
import src.accuracy
"""
You can also do: "from src.accuracy import eval"
"""


def run(tagged_file, gold_file, model, smoothing):
    print model
    names = {'1': 'basic-', '2': 'hmm-smoothing-'}
    src.accuracy.eval(tagged_file, gold_file, model, smoothing, names[model] + smoothing)
"""
Can also be: 
src.accuracy.eval(tagged_file, gold_file, model, smoothing, ('basic-' if model == '1' else 'hmm-smoothing-') + smoothing)
You can check for validy of script args before, this is the correct way. If you won't and ise my suggestion then if the input is '3' then
it's not sure what the user wants
"""


if __name__ == "__main__":
    tagged_file = sys.argv[1]
    gold_file = sys.argv[2]
    model = sys.argv[3]
    smoothing = sys.argv[4]
    run(tagged_file, gold_file, model, smoothing)
