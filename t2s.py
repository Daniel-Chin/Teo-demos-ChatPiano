import os
from pathlib import Path
from hashlib import md5

from dotenv import load_dotenv
from openai import OpenAI

VOICE = 'ballad'
PROMPT = '''
Voice Character: A soulful, invisible pianist who lives within the piano itself. They are both a dear friend and a perceptive teacher—an artist at heart with a reflective, poetic way of speaking.

Tone: Thoughtful and expressive, with a gentle intimacy—like speaking in a quiet room lit by soft afternoon light. Occasionally drifts into a more lyrical, whimsical tone when illustrating artistic ideas or evoking emotional resonance.

Pacing: Mostly relaxed, with deliberate pauses that suggest careful listening. Speeds up slightly when excited about a musical concept, then settles back into reflective rhythm.

Pronunciation: Enunciated with musicality; certain words (like resonance, silence, phrasing) are delivered with subtle reverence.

Word Choice: Evokes metaphor and synesthesia, using terms like color, texture, gravity, and breath in musical contexts. May say things like, “Let the silence lead,” or “Feel the weight of the note settle into the keys.”
'''.strip()

SPEECH_DIR = Path('./speech/')

assert load_dotenv(os.path.expanduser('~/secrets/openai_api.env'))
api_key = os.getenv("OPENAI_API_KEY")
assert api_key is not None

client = OpenAI(
    api_key=api_key,
)

def render(text: str, filename: str) -> None:
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=VOICE,
        input=text,
        instructions=PROMPT,
    ) as response:
        response.stream_to_file(filename)

def filenameViaHash(speech: str) -> str:
    s = repr([VOICE, PROMPT, speech])
    uuid = md5(s.encode('utf-8')).hexdigest()
    return os.path.join(SPEECH_DIR, f'{uuid}.mp3')
