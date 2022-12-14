# Author: Sean Cruikshank

# Code References:
# OpenAI API documention - https://beta.openai.com/docs/introduction
# Text to Speech coverter blog - https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/


#TODO: research how to make conversation more natural (request ChatGPT to respond with a question)
#TODO: different modes? conversation mode, question answer mode, ask a random question etc
#TODO: split code into smaller functions for maintainibility
#TODO: clean up print statements
#TODO: ChatGPT model config option


import os 
import openai
import speech_recognition as sr
import pyttsx3
import config
import logging


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
            user_prompt = user_recorder.recognize_google(prompt_audio)
            user_prompt = user_prompt.lower()

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        logger.error("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown value occured in recording")
        logger.error("unknown value occured in recording")

    return user_prompt


def request_completion(user_recorder): 


    while True:
        
        user_prompt = 0
        prompt_text = define_speech_prompt(user_prompt, user_recorder)
        print(prompt_text)
        logger.info("prompt text provided: " + prompt_text)
        
        if prompt_text == "stop":
            logger.info("user 'stop' command recorded")
            break
        
        elif prompt_text != "stop":
            max_tokens_setting = config.max_tokens
            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_text,
                max_tokens=max_tokens_setting)
            print(completion.choices[0].text)
            logger.info("ChatGPT API responded with the following completion: " + completion.choices[0].text)
            speak_text(completion.choices[0].text)
            continue
        
        else:
            print("something went wrong") 


    

def main():

    # retrieve api key from OS environment variables
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    # define speech recorder
    user_recorder = sr.Recognizer()
    
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

    # greeting + pass to user input function
    #speak_text("Greetings from Leaf village, I am soo nah dae, the fifth hoe kag ae, please ask me anything.")
    speak_text("Greetings from Leaf village, I am the Hokage, please ask me anything.")
    request_completion(user_recorder)
        

if __name__ == "__main__":
    main()
