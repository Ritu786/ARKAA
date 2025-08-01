import logging

def set_logger(name:str):
    '''
    Configure Logging for the application.

    Args:
        name (str): 
    '''
    # Entry point for Logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # File Handler -- Output to File, Only Logs above DEBUG Level
    file_handler = logging.FileHandler('./core/app.log')
    file_handler.setLevel(logging.DEBUG)

    # Console Handler -- Output to console, Only Logs above INFO Level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter -- Formats the Output Logs
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Adding Handler to the logs
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

     