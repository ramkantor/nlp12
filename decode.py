import sys
import src.BasicTagger
import src.HmmDecoder


def run(model, test_file, param_file_1, param_file_2):
    print model
    methods = {
        '1': src.BasicTagger.decode,
        '2': src.HmmDecoder.decode
    }

    methods[model](test_file, param_file_1, param_file_2)


if __name__ == "__main__":
    model = sys.argv[1]
    test_file = sys.argv[2]
    param_file_1 = sys.argv[3]
    param_file_2=None
    if len(sys.argv) > 4:
        param_file_2 = sys.argv[4]
    run(model, test_file, param_file_1, param_file_2)
