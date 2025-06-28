import typing as tp
from subprocess import Popen, DEVNULL

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

def playAudio(filename: str):
    with Popen(
        ['ffplay', '-nodisp', '-autoexit', filename], 
        stdout=DEVNULL, stderr=DEVNULL, 
    ) as proc:
        proc.wait()

def main():
    for lines in Collate():
        for line in lines:
            print(line)
        for line in lines:
            if line.subject != 'Teo':
                input('Press Enter to continue...')
                continue
            if line.speech is not None:
                filename = filenameViaHash(line.speech)
                playAudio(filename)
                continue
            assert line.action is not None
            # todo: investigate multi-device audio output
            ...

if __name__ == '__main__':
    main()
