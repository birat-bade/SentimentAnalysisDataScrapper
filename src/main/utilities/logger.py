import logging
from src.config.config import Config


class Logger:
    log_path = Config.log_path
    logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', level=logging.INFO,
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    @staticmethod
    def add_log(log):
        logging.info(log)

    @staticmethod
    def add_error(error):
        logging.error(error)
