import os
import logging
import project_conf
import time
from m_main import get_testlog_path

def start_log(text_view=None):
    log_path = get_testlog_path(project_conf.PROJECT_SN)
    # 屏幕显示输出log
    pr = logging.StreamHandler()
    # 将log输出至文件
    file = logging.FileHandler(log_path, 'w+')
    logging.basicConfig(level=logging.INFO, handlers=[pr,file],
                        format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
                        )

def get_log(func):
    def inner(*args, **kwargs):
        logging.info('Begin Test %s' % func.__name__)
        func(*args, **kwargs)
        logging.info('Finished Test %s' % func.__name__)

    return inner

