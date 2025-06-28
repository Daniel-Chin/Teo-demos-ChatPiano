import typing as tp
from subprocess import Popen

from script_iter import ScriptIter, Line
from t2s import filenameViaHash

def Collate():
    buf: tp.List[Line] = []
    for line in ScriptIter():
        buf.append(line)
        if line.subject != 'Teo':
            yield buf
            buf = []
    if buf:
        yield buf

def main():
    for lines in Collate():
        for line in lines:
            print(line)
        for line in lines:
            if line.subject != 'Teo':
                continue
            if line.speech is not None:
                ...


if __name__ == '__main__':
    main()
