import os
import logging

def startLog():
    # 屏幕显示输出log
    log_main_dir = r'D:\mytools\SmokingTestCase'
    pr = logging.StreamHandler()
    filename = os.path.join(log_main_dir,'runlog','runlog.log')
    # 将log输出至文件
    file = logging.FileHandler(filename, 'w+')

    # 配置Log
    # logging.basicConfig(level=logging.INFO, handlers=[pr, file],
    #                     format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
    #                            "-----modelName=%(filename)s,funcName=%(funcName)s,codeLine=%(lineno)s ",
    #                     )
    logging.basicConfig(level=logging.INFO, handlers=[pr, file],
                        format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
                        )

def get_log(func):
    def inner(*args,**kwargs):
        logging.critical('begin test %s'%func.__name__)
        func(*args,**kwargs)
        logging.critical('Finished test %s'%func.__name__)
    return inner
