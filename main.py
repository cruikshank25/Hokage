# Author: Sean Cruikshank
# built using OpenAI API docs 
# and https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/

import os 
import openai
import speech_recognition as sr
import pyttsx3

# get openai key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

# initialise speech recogniser
r = sr.Recognizer()

# function to convert text to speech
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# function to take user speech input and return string
def defineSpeechPrompt():

    global myPrompt
    myPrompt = 0
    while myPrompt == 0:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                promptAudio = r.listen(source)
                myPrompt = r.recognize_google(promptAudio)
                myPrompt = myPrompt.lower()
                print("did you say ",myPrompt)
                SpeakText("did you say")
                SpeakText("please answer yes or no")
                SpeakText(myPrompt)
                confirmationAudio = r.listen(source)
                myConfirmation = r.recognize_google(confirmationAudio)
                myConfirmation = myConfirmation.lower()
                if myConfirmation == "yes":
                    SpeakText("thank you for confirming, give me a moment to answer your question")
                    return myPrompt
                elif myConfirmation == "no":
                    SpeakText("sorry I did not understand, can you please try again")
                    defineSpeechPrompt()
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred")

SpeakText("Good Day, I am the Hokage, please ask me anything")
defineSpeechPrompt()

# create a completion 
completion = openai.Completion.create(engine="text-davinci-003", prompt=myPrompt, max_tokens=32)

# print the completion
print(completion.choices[0].text)

# speak the completion
SpeakText(completion.choices[0].text)
