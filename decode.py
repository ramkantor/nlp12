import sys
import src.BasicTagger
import src.HmmDecoder


def run(model, test_file, param_file_1, param_file_2):
    print model
    methods = {
        '1': src.BasicTagger.decode,
        '2': src.HmmDecoder.decode
    }
"""
"run" is a little ambiguous. What if you had 2 run functions from different modules (imported as the functions and not the modules)
Something more understandable than '1', '2'.
You can have a "methods" dictionary in a separate file. This way it won't be computed every time you apply "run", even though
it's done only once. But the idea of a model(/methods) dict' is correct, and would have fit even more if there were more than 2 models.
Otherwise it can also be:
(src.BasicTagger.decode if model == '1' else src.HmmDecoder.decode)(test_file, param_file_1, param_file_2)
"""

    methods[model](test_file, param_file_1, param_file_2)


if __name__ == "__main__":
    model = sys.argv[1]
    test_file = sys.argv[2]
    param_file_1 = sys.argv[3]
    param_file_2=None
    if len(sys.argv) > 4:
        param_file_2 = sys.argv[4]
"""
param_file_2 = sys.argv[4] if len(sys.argv) > 4 else None
"""
    run(model, test_file, param_file_1, param_file_2)
