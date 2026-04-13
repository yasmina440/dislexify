import pyttsx3
import threading
import time
from kivy.clock import Clock

engine = pyttsx3.init()
engine.setProperty('rate', 160)

is_playing = False


def speak_with_highlight(text, on_word=None, on_end=None):
    global is_playing
    is_playing = True

    words = text.split()

    def run():
        global is_playing

        for word in words:
            if not is_playing:
                break

            engine.say(word)
            engine.runAndWait()

            if on_word:
                Clock.schedule_once(lambda dt, w=word: on_word(w))

            time.sleep(0.05)

        is_playing = False

        if on_end:
            Clock.schedule_once(lambda dt: on_end())

    threading.Thread(target=run).start()


def stop():
    global is_playing
    engine.stop()
    is_playing = False


def toggle(text, on_word=None, on_end=None):
    global is_playing

    if is_playing:
        stop()
    else:
        speak_with_highlight(text, on_word, on_end)