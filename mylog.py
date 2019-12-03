import os
import logging
import project_conf
import time


def start_log(text_view=None):
    # 屏幕显示输出log
    tformat = '%Y_%m_%d_%H%M%S'
    mytime = time.strftime(tformat, time.localtime())
    pr = logging.StreamHandler()
    # 将log输出至文件
    file = logging.FileHandler(project_conf.LOG_PATH, 'w+')
    logging.basicConfig(level=logging.INFO, handlers=[pr,file],
                        format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
                        )


def get_log(func):
    def inner(*args, **kwargs):
        logging.info('Begin Test %s' % func.__name__)
        func(*args, **kwargs)
        logging.info('Finished Test %s' % func.__name__)

    return inner

