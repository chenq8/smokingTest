import os
import logging
import project_conf
import time
def startLog():
    # 屏幕显示输出log
    tformat = '%Y_%m_%d_%H%M%S'
    mytime = time.strftime(tformat, time.localtime())
    pr = logging.StreamHandler()
    filename = os.path.join(project_conf.PROJECT_PATH,'runlog','%s_%s_log.log'%(mytime,project_conf.PROJECT_SN))
    # 将log输出至文件
    file = logging.FileHandler(filename, 'w+')

    logging.basicConfig(level=logging.INFO, handlers=[pr, file],
                        format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
                        )

def get_log(func):
    def inner(*args,**kwargs):
        logging.critical('begin test %s'%func.__name__)
        func(*args,**kwargs)
        logging.critical('Finished test %s'%func.__name__)
    return inner
