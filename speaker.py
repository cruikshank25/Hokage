#INFO: MacOS doesn't support 'voices' configuration in pyttsx3

import pyttsx3
import config

def speak_text(command):
    engine = pyttsx3.init()
    #voices = engine.getProperty('voices')
    #engine.setProperty('voice', voices[config.voice].id)
    engine.setProperty('rate', 200)
    engine.say(command)
    engine.runAndWait()