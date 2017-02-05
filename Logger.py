import logging


class Logger:
    def __init__(self, name):
        self.name = name
        self._config()

    def start(self):
        pass

    def stop(self):
        pass

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def _config(self):
        self.logger = logging.getLogger(self.name)
        # dir = os.path.dirname(os.path.abspath(__file__))
        filename = 'smartmirror.log'
        hdlr = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)
