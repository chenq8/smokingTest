import pytest
from runlog import testLog
import os
import logging

if __name__=='__main__':
    """脚本程序入口"""
    testLog.startLog()
    logging.info('Start smoking test')
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_contact.py','--alluredir=./allure-results'])
    os.system('allure generate '
              r'D:\mytools\SmokingTestCase\allure-results/ '
              r'-o '
              r'D:\mytools\SmokingTestCase/report '
              r'--clean')
    logging.info('Finished smoking test')

