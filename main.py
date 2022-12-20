# Author: Sean Cruikshank

# Code References:
# OpenAI API documention - https://beta.openai.com/docs/introduction
# Text to Speech coverter blog - https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/


#TODO: research how to make conversation more natural (request ChatGPT to respond with a question)
#TODO: different modes? conversation mode, question answer mode, ask a random question etc
#TODO: split code into smaller functions for maintainibility
#TODO: OpenAI model config option
#TODO: nonsense responses? Check OpenAI API docs
#TODO: investigate WhisperAI for speech to text translation (rather than Google)
#TODO: add a requirements.txt file
#TODO: Kivy for mobile app development? 

import logging
import os
import openai
import speech_recognition as sr
import pyttsx3
import config
import time
import sys
import multiprocessing as mp


def speak_text(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[config.voice].id)
    engine.say(command)
    engine.runAndWait()


def listen_for_stop(user_recorder, logger):
    while True:

        with sr.Microphone() as source:
            user_recorder.adjust_for_ambient_noise(source, duration=0.2)
            audio = user_recorder.listen(source)
            
            try:
                start_time = time.time()
                speech_text = user_recorder.recognize_google(audio)
                print(f"listen_for_stop input: {speech_text}")
                logger.info("call to Google took: %s seconds " % (time.time() - start_time))
                print(f"request_completion input: {speech_text}")

                if speech_text == "stop":
                    logger.info("user 'stop' command recorded")
                    print("stopping from 'listen_for_stop'")
                    sys.exit()

                elif speech_text != "stop":
                    continue

            except sr.UnknownValueError:
                print("Could not understand speech input 'listen_for_stop'")
            
            except sr.RequestError as e:
                print(f"Error while processing speech input 'listen_for_stop' : {e}")

            except SystemExit:
                print("sys.exit() worked as expected")
                sys.exit(1)

            except:
                print("something unknown occured")
                sys.exit(1)


def request_completion(user_recorder, logger): 
    while True:

        with sr.Microphone() as source:
            user_recorder.adjust_for_ambient_noise(source, duration=0.2)
            audio = user_recorder.listen(source)

            try:
                try: 
                    start_time = time.time()
                    speech_text = user_recorder.recognize_google(audio)
                    print("call to Google took: %s seconds " % (time.time() - start_time))
                    logger.info("call to Google took: %s seconds " % (time.time() - start_time))
                    print(f"request_completion input: {speech_text}")
                    prompt_text = str(speech_text.lower())

                except Exception as e:
                    print("call to google cloud speech to text failed with following exception: "  + e)
                    logger.error("call to google cloud speech to text failed with following exception: "  + e)

                try:
                    print("completion receives: " + prompt_text)
                    logger.info("prompt text provided: " + prompt_text)
                    
                    max_tokens_setting = config.max_tokens
                    model_setting = config.model
                    temperature_setting = config.temperature

                    completion = openai.Completion.create(
                    engine=model_setting,
                    prompt=prompt_text,
                    max_tokens=max_tokens_setting,
                    temperature=temperature_setting
                    )
                    print(completion.choices[0].text)
                    logger.info("ChatGPT responded with the following completion: " + completion.choices[0].text)
                    speak_text(completion.choices[0].text)

                except openai.APIError as e:
                    print("OpenAI API failed to process completion with the following exception: " + e)
                    logger.error("OpenAI API failed to process completion with the following exception: " + e)

            except sr.UnknownValueError:
                print("Could not understand speech input 'request_completion'")
                logger.error("unknown value occured in recording input for 'request_completion'")

            except sr.RequestError as e:
                print(f"Error while processing speech input 'request_completion' : {e}")
                logger.error("Could not request results for input ''request_completion''; {0}".format(e))


def main():
    # create a logger and make it global
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

    # create a process for each speech recognition task
    process1 = mp.Process(target=listen_for_stop, args=(user_recorder, logger))
    process2 = mp.Process(target=request_completion, args=(user_recorder, logger))

    # start the processes
    process1.start()
    process2.start()

    # cleanup and kill program if 'stop' process finishes. 
    process1.join()
    print("process1 has terminated")

    if process1.is_alive() is False:
        process2.terminate()

    process2.join()
    print("process2 has terminated")


if __name__ == "__main__":
    main()
