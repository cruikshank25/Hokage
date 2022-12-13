# Author: Sean Cruikshank
# built using OpenAI API docs 
# and https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/

import os 
import openai
import speech_recognition as sr
import pyttsx3


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def defineSpeechPrompt(myPrompt, recorder):

    myPrompt = 0
    while myPrompt == 0:
        try:
            with sr.Microphone() as source:
                recorder.adjust_for_ambient_noise(source, duration=0.2)
                promptAudio = recorder.listen(source)
                myPrompt = recorder.recognize_google(promptAudio)
                myPrompt = myPrompt.lower()

                '''
                OPTIONAL CONFIRMATION BLOCK
                UNCOMMENT THIS SECTION TO GIVE A CONFIRMATION BEFORE REQUESTING A COMPLETION

                print("did you say ",myPrompt)
                SpeakText("did you say")
                SpeakText("please answer yes or no")
                SpeakText(myPrompt)
                confirmationAudio = recorder.listen(source)
                myConfirmation = recorder.recognize_google(confirmationAudio)
                myConfirmation = myConfirmation.lower()
                if myConfirmation == "yes":
                    SpeakText("thank you for confirming, give me a moment to answer your question")
                    return myPrompt
                elif myConfirmation == "no":
                    SpeakText("sorry I did not understand, can you please try again")
                    defineSpeechPrompt(recorder)
                '''
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

    return myPrompt


def requestCompletion(recorder): 
    # create a completion and speak the result 
    
    myPrompt = 0
    promptText = defineSpeechPrompt(myPrompt, recorder)
    print(promptText)
    completion = openai.Completion.create(engine="text-davinci-003", prompt=promptText, max_tokens=64)
    print(completion.choices[0].text)
    SpeakText(completion.choices[0].text)
    SpeakText("use this knowledge from the hokage of leaf village wisely")

def main():

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    recorder = sr.Recognizer()

    SpeakText("Greetings from leaf village, I am the Hokage, please ask me anything")
    requestCompletion(recorder)


main()