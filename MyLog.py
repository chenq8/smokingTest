import os
import logging
import project_conf
import time



def startLog():
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

    logging.basicConfig(level=logging.INFO, handlers=[pr, file],
                        format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
                        )

def get_log(func):
    def inner(*args,**kwargs):
        logging.critical('begin test %s'%func.__name__)
        func(*args,**kwargs)
        logging.critical('Finished test %s'%func.__name__)
    return inner

class m_log_handler(logging.Handler):
    def __init__(self,text=None):

        self.stream = text
        logging.Handler.__init__(self)

    def emit(self, record):
        filepath = r'D:\mytools\wallpaper\test.txt'
        try:
            msg = self.format(record)
            stream = self.stream
            # issue 35046: merged two stream.writes into one.
            with open(filepath,'w+') as file:
                file.write(msg+'\n')
                self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

if __name__ == '__main__':
    startLog()
    print(pr)