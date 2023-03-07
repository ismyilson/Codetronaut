import pyttsx3


class Reader:
    """
    Text-to-speech handler.
    """

    _engine: pyttsx3.Engine

    def __init__(self, voice_index=1):
        """
        Initializes the engine and sets the voice.

        Args:
            voice_id: Sets the voice. Defaults to 1.
        """

        self._engine = pyttsx3.init()
        self._engine.setProperty('rate', 135)

        voices = self._engine.getProperty('voices')
        self._engine.setProperty('voice', voices[voice_index].id)

    def read_text(self, text, wait=True):
        """
        Converts text to speech and reads it out loud.

        Args:
            text: The string to read.
            wait: If we should wait until the text has been read. Defaults to True.
        """

        self._engine.say(text)

        if wait:
            self._engine.runAndWait()
