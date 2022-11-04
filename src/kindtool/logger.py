# https://docs.python.org/3/howto/logging.html
# https://signoz.io/docs/userguide/collect_logs_from_file/
# https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SocketHandler

import logging
import time

# logging.basicConfig(filename="./python.log", level=logging.DEBUG, datefmt='%Y-%m-%d,%H:%M:%S %z',
#                     format="{\"time\": \"%(asctime)s\", \"message\": \"%(message)s\"}", filemode="a")

# if __name__ == '__main__':
#     while True:
#         logging.debug("Logging test...")
#         logging.info("The program is working as expected")
#         logging.warning("The program may not function properly")
#         logging.error("The program encountered an error")
#         logging.critical("The program crashed")
#         time.sleep(2)

# # logger = logging.getLogger(__name__)
# # create logger
# logger = logging.getLogger('simple_example')
# logger.setLevel(logging.DEBUG)

# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# # create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# # add formatter to ch
# ch.setFormatter(formatter)

# # add ch to logger
# logger.addHandler(ch)


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
#ch = logging.NullHandler()

#fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s - %(message)s'
#fmt = "{\"time\": \"%(asctime)s\", \"level\": \"%(levelname)s\" \"message\": \"%(message)s\"}"
#datefmt='%Y-%m-%d,%H:%M:%S %z'
datefmt=None

# create formatter
formatter = logging.Formatter(datefmt=datefmt, fmt=fmt)

# add formatter to ch
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG) # level of this formater

log.addHandler(ch)



def myfunc() -> None:
    xxx = 123
    log.debug(f"Logging test... {xxx=}")
    log.info("The program is working as expected")
    log.warning("The program may not function properly")
    log.error("The program encountered an error")
    log.critical("The program crashed")

    log.debug("i am a debug...")
    log.setLevel(logging.INFO)
    log.debug("i am silent")

    try:
        log.warning("crashing time...")
        raise Exception("i crashed")
    except Exception as ex:
        #log.exception(f"oops {ex=}")
        log.exception(ex)


if __name__ == '__main__':
    log.debug(f"App start")
    myfunc()