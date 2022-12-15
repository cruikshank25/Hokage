# Author: Sean Cruikshank

# Code References:
# OpenAI API documention - https://beta.openai.com/docs/introduction
# Text to Speech coverter blog - https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/


#TODO: research how to make conversation more natural (request ChatGPT to respond with a question)
#TODO: different modes? conversation mode, question answer mode, ask a random question etc
#TODO: split code into smaller functions for maintainibility
#TODO: clean up print statements
#TODO: ChatGPT model config option
#TODO: error handling for unrecognised recording input
#TODO: error handling for bad responses from chatGPT 
#TODO: listen for stops when speaking response (needs to be interuptable) 
#TODO: nonsense responses? Check OpenAI API docs

import logging
import os
import openai
import speech_recognition as sr
import pyttsx3
import config
import time
import sys


def speak_text(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[config.voice].id)
    engine.say(command)
    engine.runAndWait()


def define_speech_prompt(user_prompt, user_recorder):
    try:
        with sr.Microphone() as source:
            user_recorder.adjust_for_ambient_noise(source, duration=0.2)
            prompt_audio = user_recorder.listen(source)
            start_time = time.time()
            user_prompt = user_recorder.recognize_google(prompt_audio)
            print("--- %s seconds ---" % (time.time() - start_time))
            logger.info("call to Google took: %s seconds " % (time.time() - start_time))
            user_prompt = user_prompt.lower()
            user_prompt = str(user_prompt)
            print("define prompt creates: " + user_prompt)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        logger.error("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown value occured in recording")
        logger.error("unknown value occured in recording")
        #define_speech_prompt(user_prompt, user_recorder)
        request_completion(user_recorder)

    print("before return: " + str(user_prompt) )
    return user_prompt


def request_completion(user_recorder): 
    while True:
        
        user_prompt = 0
        prompt_text = define_speech_prompt(user_prompt, user_recorder)
        prompt_text = str(prompt_text)
        print("completion receives: " + prompt_text)
        logger.info("prompt text provided: " + prompt_text)
        
        if prompt_text == "stop":
            logger.info("user 'stop' command recorded")
            print("stopping from local")
            sys.exit()
        
        elif prompt_text == "0":
            print("an invalid numeric string was supplied, try again")
            logger.info("an invalid numeric string was supplied, try again")
            #speak_text("an invalid value was detected please try again")
            request_completion(user_recorder)

        elif prompt_text != "stop":
            max_tokens_setting = config.max_tokens
            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_text,
                max_tokens=max_tokens_setting)
            print(completion.choices[0].text)
            logger.info("ChatGPT responded with the following completion: " + completion.choices[0].text)
            speak_text(completion.choices[0].text)
            continue
        
        else:
            print("something went wrong") 


def main():

    # create a logger and make it global
    global logger
    logger = logging.getLogger("my_logger")
    # set the log level (from the config file)
    logging_level = config.logging_level
    logger.setLevel(logging_level)
    # create a file handler
    file_handler = logging.FileHandler("hokage_log.txt")
    # create a formatter and set it for the file handler
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    # add the file handler to the logger
    logger.addHandler(file_handler)

    # retrieve api key from OS environment variables
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    # define speech recorder
    user_recorder = sr.Recognizer()

    # greeting + pass to user input function
    #speak_text("Greetings from Leaf village, I am soo nah dae, the fifth hoe kag ae, please ask me anything.")
    speak_text("Greetings from Leaf village, I am the Hokage, please ask me anything.")
    request_completion(user_recorder)


if __name__ == "__main__":
    main()
