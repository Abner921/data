#encoding=utf-8
import logging
import os
from datetime import date


def initLogger():
    logger = logging.getLogger("sem")
    logger.setLevel(logging.DEBUG)

    #FileHandler
    baseDir = os.path.split(os.path.realpath(__file__))[0]
    logdir = os.path.join(baseDir,'..','log',date.today().strftime('%Y-%m/%d'))
    logname = "sem-baidu.log"

    if not os.path.isdir(logdir):
            os.makedirs(logdir)
    logpath = os.path.join(logdir,logname)

    fh = logging.FileHandler(logpath)
    fh.setLevel(logging.INFO)

    #StreamHandler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    #formatter
    formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    #addHandler
    logger.addHandler(ch)
    logger.addHandler(fh)

    #logger.info("test")  #for test

    return logger

initlogger = initLogger()
def getLogger(name=None):
    if name is None:
        return initlogger
    logger = logging.getLogger("sem"+'.'+name)
    return logger


