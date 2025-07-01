import os
import typing as tp
from subprocess import Popen, DEVNULL
from contextlib import contextmanager

import mido

import playMidi

from script_iter import ScriptIter, Line
from t2s import filenameViaHash

SPEECH = (0, 0, 'alsa_output.usb-BEHRINGER_UMC404HD_192k-00.HiFi__Line1__sink')
MUSIC_AUDIO = (0, 0, 'alsa_output.pci-0000_00_1f.3.analog-stereo')

def Collate():
    buf: tp.List[Line] = []
    for line in ScriptIter():
        buf.append(line)
        if line.subject != 'Teo':
            yield buf
            buf = []
    if buf:
        yield buf

def remapVelocity(x: int):
    if x == 0:
        return 0
    return max(0, min(127, round((x - 40) * 1.5)))

def playAudio(filename: str, card_i: int, device_i: int, sink: str):
    env = os.environ.copy()
    env['PULSE_SINK'] = sink
    with Popen(
        [
            'ffplay', '-nodisp', '-autoexit', 
            # '-ao', f'alsa:device=hw={card_i},{device_i}',
            filename, 
        ], 
        stdout=DEVNULL, stderr=DEVNULL, env=env, 
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
    output_name = playMidi.askOutput()
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
                playMidi.main(
                    './music/huaxin.mid', 
                    output_name, velocity_remap=remapVelocity,
                )
            elif line.action == 'huaxin_simple':
                playMidi.main(
                    './music/huaxin_simple.mid', 
                    output_name, velocity_remap=remapVelocity,
                )
            else:
                raise ValueError(f'unknown {line.action = }')

if __name__ == '__main__':
    main()
