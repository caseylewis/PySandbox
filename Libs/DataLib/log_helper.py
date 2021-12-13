import logging
import os

# DEFAULT LOG FORMATTER
default_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO, formatter=default_formatter):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def delete_logger(log_file, logger):
    """

    :param log_file: Filepath of log file
    :param logger: Logger instance that needs to be deleted
    :return: None
    """
    # handler = logging.FileHandler(log_file)
    # logger.removeHandler(handler)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    try:
        os.remove(log_file)
    except Exception as e:
        print(e)


def folder_exists(folder_path):
    """To check if a folder exists"""
    return os.path.isdir(folder_path)


class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text
        self.text.config(state=DISABLED)

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state=NORMAL)
            self.text.insert(END, msg + '\n')
            self.text.configure(state=DISABLED)
            # Autoscroll to the bottom
            self.text.yview(END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)
