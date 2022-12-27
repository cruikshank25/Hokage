# Author: Sean Cruikshank
#TODO: different modes? conversation mode, question answer mode, ask a random question etc
#TODO: handle nonsense responses such as code
#TODO: mobile app dev? Kivy? 
#TODO: Web app? Flask? Django? 
#TODO: add user google key for speech to text api (rather than libs default)

import log
import os
import openai
import speech_recognition as sr
import speaker
import config
import time
import sys
import multiprocessing as mp


def listen_for_stop(user_recorder):
    while True:
        print('process 1 started...')
        logger = log.custom_logger()
        logger.info('process 1 started...')

        with sr.Microphone() as source:
            logger.info('process 1 mic adjusting for ambient noise...')
            print('process 1 mic adjusting for ambient noise...')
            user_recorder.adjust_for_ambient_noise(source, duration=0.2)

            logger.info('process 1 starting listener...')
            print('process 1 starting listener...')
            audio = user_recorder.listen(source)
            
            try:
                logger.info('process 1 listening...')
                print('process 1 listening...')
                start_time = time.time()
                speech_text = user_recorder.recognize_google(audio, language='en-GB')
                logger.info('process 1 Google Speech-to-Text recognition took: %s seconds ' % (time.time() - start_time))
                print('process 1 Google Speech-to-Text recognition took: %s seconds ' % (time.time() - start_time))
                print(f'process 1 listen_for_stop input: {speech_text}')

                if speech_text == 'stop':
                    logger.info('user "stop" command recorded')
                    print('stopping from "listen_for_stop"')
                    sys.exit(1)

                elif speech_text != 'stop':
                    continue

            except sr.UnknownValueError:
                print('Could not understand speech input "listen_for_stop"')
            
            except sr.RequestError as e:
                print(f'Error while processing speech input "listen_for_stop" : {e}')

            except SystemExit:
                print('sys.exit(1) worked as expected')
                sys.exit(1)

            except:
                print('something unknown occured')
                sys.exit(1)


def request_completion(user_recorder): 
    while True:
        print('process 2 started...')
        logger = log.custom_logger()
        logger.info('process 2 started...')

        with sr.Microphone() as source:
            logger.info('process 2 mic adjusting for ambient noise...')
            print('process 2 mic adjusting for ambient noise...')
            user_recorder.adjust_for_ambient_noise(source, duration=0.2)
            
            logger.info('process 2 starting listener...')
            print('process 2 starting listener...')
            audio = user_recorder.listen(source)


            try:
                logger.info('process 2 listening...')
                print('process 2 listening...')

                try: 
                    start_time = time.time()
                    speech_text = user_recorder.recognize_google(audio, language='en-GB')
                    logger.info('process 2 Google Speech-to-Text recognition took: %s seconds ' % (time.time() - start_time))
                    print('process 2 Google Speech-to-Text recognition took: %s seconds ' % (time.time() - start_time))
                    print(f'process 2 request_completion input: {speech_text}')
                    prompt_text = str(speech_text.lower())

                    try:
                        print('completion receives: ' + prompt_text)
                        logger.info('prompt text provided: ' + prompt_text)
                        
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
                        logger.info('OpenAI responded with the following completion: ' + completion.choices[0].text)
                        speaker.speak_text(completion.choices[0].text)

                    except openai.APIError as e:
                        print('OpenAI API failed to process completion with the following exception: ' + e)
                        logger.error('OpenAI API failed to process completion with the following exception: ' + e)

                except Exception as e:
                    print('Google API failed with following exception: '  + str(e))
                    logger.error('Google API failed with following exception: '  + str(e))

            except sr.UnknownValueError:
                print('Could not understand speech input "request_completion"')
                logger.error('unknown value occured in recording input for "request_completion"')

            except sr.RequestError as e:
                print(f'Error while processing speech input "request_completion" : {e}')
                logger.error('Could not request results for input "request_completion"; {0}'.format(e))


def main():

    # initialise logger
    logger = log.custom_logger()
    logger.info('custom logger initialised')

    # retrieve api key from OS environment variables
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    # define speech recorder
    user_recorder = sr.Recognizer()

    # create a process for each speech recognition task
    process1 = mp.Process(target=listen_for_stop, args=(user_recorder,))
    process2 = mp.Process(target=request_completion, args=(user_recorder,))

    # start the processes
    process1.start()
    process2.start()

    # greeting + pass to user input function
    #speaker.speak_text("Greetings from Leaf village, I am soo nah dae, the fifth hoe kag ae, please ask me anything.")
    speaker.speak_text('Greetings, please ask me anything.')

    # monitor the processes every second, if one stops, then terminate the program
    while process1.is_alive() and process2.is_alive():
        process1.join()
        if not process1.is_alive():
            process2.terminate()
            print('process2 terminating...')
            logger.info('process2 terminating...')
        process2.join()
        if not process2.is_alive():
            process1.terminate()
            print('process1 terminating...')
            logger.info('process1 terminating...')

if __name__ == '__main__':
    main()
