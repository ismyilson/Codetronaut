import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 135)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def read_text(text):
    engine.say(text)
    engine.runAndWait()
