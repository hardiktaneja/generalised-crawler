import logging
from logging.handlers import TimedRotatingFileHandler as tfh
import os


class loggerClass(str):
    _main_log = None

    def __new__(cls, filename=None):
        if not cls._main_log:
            cls._main_log = str.__new__(cls, filename)
        return cls._main_log

    def __init__(self, filename=None):
        try:
            if filename and not hasattr(self, 'logger'):
                log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                             'logs/', filename)
                try:
                    os.makedirs(os.path.dirname(log_file_path))
                except:
                    pass

                self.logger = logging.getLogger(filename)
                self.logger.setLevel(logging.INFO)
                if not self.logger.handlers:
                    fh = tfh(log_file_path, when='midnight', interval=1, utc=True, backupCount=7)
                    fh.setFormatter(
                        logging.Formatter(
                            "%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"))
                    self.logger.addHandler(fh)

        except:
            logging.error('Logger failed', exc_info=True)
            raise
