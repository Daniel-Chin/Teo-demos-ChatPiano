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
            l, r = line.split(':', 1)
            subject = l.strip()
            speech = r.strip().strip('"')
