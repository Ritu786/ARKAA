import logging 

def set_logger(name:str):
    '''
    Configure Logging for the Application.
    '''
    # Entry point for Logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # File Handler
    file_handler = logging.FileHandler('./app_utils/app.log')
    file_handler.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Adding Handler to the Logs
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger