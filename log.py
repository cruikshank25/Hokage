import logging
import config

def custom_logger():

    # create a logger
    logger = logging.getLogger('my_logger')
    
    # set the log level (from the config file)
    logging_level = config.logging_level
    logger.setLevel(logging_level)
    
    # create a file handler
    file_handler = logging.FileHandler('hokage_log.txt')
    
    # create a formatter and set it for the file handler
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    
    # add the file handler to the logger
    logger.addHandler(file_handler)

    return logger