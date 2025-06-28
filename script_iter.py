from dataclasses import dataclass

SCRIPT = './script.md'

@dataclass(frozen=True)
class Line:
    subject: str
    speech: str | None
    action: str | None

    def __post_init__(self):
        assert (self.speech is None) != (self.action is None)
        assert self.subject in ('Teo', 'John')
    
    def __repr__(self):
        if self.speech is not None:
            return f'{self.subject}: "{self.speech}"'
        else:
            return f'{self.subject}: [{self.action}]'

def ScriptIter():
    with open(SCRIPT, 'r', encoding='utf-8') as f:
        linesIter = iter(f)
        heading = next(linesIter)
        assert heading.startswith('# ')
        print(heading.strip())
        for line in linesIter:
            line = line.strip()
            if not line:
                continue
            left, right = line.split(':', 1)
            subject = left.strip()
            speech_action = right.strip().strip('"')
            if subject == 'John':
                yield Line(subject, speech_action, None)
            else:
                while True:
                    try:
                        speech, more = speech_action.split('[', 1)
                    except ValueError:
                        speech = speech_action.strip()
                        if speech:
                            yield Line(subject, speech, None)
                        break
                    else:
                        yield Line(subject, speech.strip(), None)
                        action, speech_action = more.split(']', 1)
                        yield Line(subject, None, action.strip())
                        speech_action = speech_action.strip()
                        if not speech_action:
                            break

if __name__ == '__main__':
    print(*ScriptIter(), sep='\n\n')
