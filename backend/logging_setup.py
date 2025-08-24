import logging

def setup_logger(name,log_file='main.log',level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # custom_logger
    logger = logging.getLogger(name)
    # configure_custom_logger
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger