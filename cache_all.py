from os import path

from tqdm import tqdm

from script_iter import ScriptIter
from t2s import render, filenameViaHash

def main():
    for line in tqdm([*ScriptIter()], desc='t2s'):
        if line.subject != 'Teo':
            continue
        if line.speech is None:
            continue
        filename = filenameViaHash(line.speech)
        if path.exists(filename):
            continue
        render(line.speech, filename)

if __name__ == '__main__':
    main()
