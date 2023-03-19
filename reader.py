import pyttsx3


_engine = pyttsx3.init()
_engine.setProperty('rate', 135)

_voices = _engine.getProperty('voices')
_engine.setProperty('voice', _voices[1].id)


def read_text(text, wait=True):
    _engine.say(text)

    if wait:
        _engine.runAndWait()
