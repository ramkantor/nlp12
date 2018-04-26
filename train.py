import sys
import src.BasicTagger
import src.HmmTagger


def run(model, file, smoothing):
    print model
    methods = {
        '1': src.BasicTagger.train,
        '2': src.HmmTagger.train
    }

    methods[model](file, smoothing)


if __name__ == "__main__":
    model = sys.argv[1]
    file = sys.argv[2]
    smoothing = sys.argv[3]
    smooth={'y':True, 'n':False}[smoothing]
    run(model, file, smooth)
    
    """
    run(model, file, smoothing == 'y')
    """
