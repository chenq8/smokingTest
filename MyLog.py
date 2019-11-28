import os
import logging
import project_conf
import time
import myui

def startLog(text_view=None):
    # 屏幕显示输出log
    tformat = '%Y_%m_%d_%H%M%S'
    mytime = time.strftime(tformat, time.localtime())
    log_path = os.path.join(project_conf.PROJECT_PATH,
                            'test_log')
    pr = logging.StreamHandler()
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    filename = os.path.join(log_path,
                            '%s_%s_log.log' %
                            (mytime,project_conf.PROJECT_SN))

    # 将log输出至文件
    file = logging.FileHandler(filename, 'w+')
    if text_view:
        t = MyLogHandler(text_view)
        logging.basicConfig(level=logging.INFO, handlers=[pr,file,t],
                        format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
                        )
    else:

        logging.basicConfig(level=logging.INFO, handlers=[pr,file,],
                            format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
                            )
def start_log():
    tformat = '%Y_%m_%d_%H%M%S'
    mytime = time.strftime(tformat, time.localtime())
    log_path = os.path.join(project_conf.PROJECT_PATH,
                            'test_log')
    my_log = logging.getLogger('main')
    my_log.setLevel(logging.DEBUG)
    format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    filename = os.path.join(log_path,
                            '%s_%s_log.log' %
                            (mytime, project_conf.PROJECT_SN))

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(format)
    # 将log输出至文件
    file = logging.FileHandler(filename, 'w+')
    file.setLevel(logging.DEBUG)
    file.setFormatter(format)

    my_log.addHandler(console)
    my_log.addHandler(file)

def get_log(func):
    def inner(*args,**kwargs):
        logging.info('begin test %s'%func.__name__)
        func(*args,**kwargs)
        logging.info('Finished test %s'%func.__name__)
    return inner

class MyLogHandler(logging.Handler):

    terminator = '\n'

    def __init__(self, my_obj):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        logging.Handler.__init__(self)

        self.stream = my_obj

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream

            stream.insert('end',msg + self.terminator)
            stream.see('end')
            # stream.updata()
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

if __name__ == '__main__':
    startLog()
    print(pr)