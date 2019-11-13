import pytest
from runlog import testLog
import os
import logging

if __name__=='__main__':
    """脚本程序入口"""
    testLog.startLog()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase','--alluredir=./allure-results'])
    logging.info('run done')
    os.system('allure generate '
              r'D:\mytools\SmokingTestCase\allure-results/ '
              r'-o '
              r'D:\mytools\SmokingTestCase\allure-results/report '
              r'--clean')
    logging.info('report done')
