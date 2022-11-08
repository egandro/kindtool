# https://docs.python.org/3/howto/logging.html
# https://signoz.io/docs/userguide/collect_logs_from_file/
# https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SocketHandler
# https://stackoverflow.com/questions/28180159/how-do-i-can-format-exception-stacktraces-in-python-logging

import logging
from typing import Any

level: any = -1
loggers: any = []

def setLevel(lev: Any) -> None:
    global level
    global loggers
    level = lev

    if loggers:
        for log in loggers:
            log.setLevel(lev)
            if log.hasHandlers():
                for handler in log.handlers:
                    handler.setLevel(lev)

def getLogger(name: str) -> logging.Logger:
    log = logging.getLogger(name)
    # todo only set StreamHanlder if loglevel was set
    # ch = logging.NullHandler()
    ch = logging.StreamHandler()
    if level >0:
        log.setLevel(level)

    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s - %(message)s'
    datefmt=None

    # create formatter
    formatter = logging.Formatter(datefmt=datefmt, fmt=fmt)

    # add formatter to ch
    ch.setFormatter(formatter)
    ch.setLevel(level)
    log.addHandler(ch)

    loggers.append(log)

    return log
