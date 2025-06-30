import typing as tp
from subprocess import Popen, DEVNULL
from contextlib import contextmanager

import mido
import mido.backends

from script_iter import ScriptIter, Line
from t2s import filenameViaHash

SPEECH = (0, 0)
MUSIC_AUDIO = (0, 0)

def Collate():
    buf: tp.List[Line] = []
    for line in ScriptIter():
        buf.append(line)
        if line.subject != 'Teo':
            yield buf
            buf = []
    if buf:
        yield buf

def playAudio(filename: str, card_i: int, device_i: int):
    with Popen(
        [
            'ffplay', '-nodisp', '-autoexit', 
            '-ao', f'alsa:device=hw={card_i},{device_i}',
            filename, 
        ], 
        stdout=DEVNULL, stderr=DEVNULL, 
    ) as proc:
        proc.wait()

@contextmanager
def MidoContext():
    output_names: tp.List[str] = mido.get_output_names()  # type: ignore
    print('MIDI output:')
    print(*enumerate(output_names), sep='\n')
    device_i = int(input('Select:'))
    name = output_names[device_i]
    with mido.open_output(name) as outPort:   # type: ignore
        outPort: mido.ports.BaseOutput

        def playMidi(filename: str):
            mid = mido.MidiFile(filename)
            for msg in mid.play():
                outPort.send(msg)
        
        yield playMidi

def main():
    with MidoContext() as playMidi:
        for lines in Collate():
            for line in lines:
                print(line)
            for line in lines:
                if line.subject != 'Teo':
                    input('Press Enter to continue...')
                    continue
                if line.speech is not None:
                    filename = filenameViaHash(line.speech)
                    playAudio(filename, *SPEECH)
                    continue
                assert line.action is not None
                if line.action == 'mars':
                    playAudio('./music/mars.wav', *MUSIC_AUDIO)
                elif line.action == 'neptune':
                    playAudio('./music/neptune.wav', *MUSIC_AUDIO)
                elif line.action == 'jupiter':
                    playAudio('./music/jupiter.wav', *MUSIC_AUDIO)
                elif line.action == 'huaxin':
                    playMidi('./music/huaxin.mid')
                else:
                    raise ValueError(f'unknown {line.action = }')

if __name__ == '__main__':
    main()
