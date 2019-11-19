import os
import logging

def startLog():
    # 屏幕显示输出log
    pr = logging.StreamHandler()
    filename = os.path.join(r'D:\mytools\SmokingTestCase','runlog','runlog.log')
    # 将log输出至文件
    file = logging.FileHandler(filename, 'w+')

    # 配置Log
    logging.basicConfig(level=logging.INFO, handlers=[pr, file],
                        format="%(asctime)s,%(name)s,%(levelname)s : %(message)s"
                               "-----modelName=%(filename)s,funcName=%(funcName)s,codeLine=%(lineno)s ",
                        )