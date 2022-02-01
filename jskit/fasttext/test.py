from .config import test_file_path
from .fasttext_classifier import FasttextClassifierBase

if __name__ == '__main__':
    classifier = FasttextClassifierBase()

    print('')
    print('TESTING')
    with open(test_file_path, 'r', encoding='utf-8') as input_file:
        tests = [ln.strip() for ln in input_file.readlines() if ln.strip()]

    result = classifier.predict(tests)
    print(result)
    print('-' * 20)
