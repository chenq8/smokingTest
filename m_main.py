import os
import logging
import subprocess
import time
from multiprocessing import Process, Value

import allure
from adbutils import adb
import pytest
import mylog
import project_conf
from threading import Thread
from subprocess import Popen, PIPE
import myui
from page import base
import sys

# def resource_path():
#     if getattr(sys, 'frozen', False):  # 是否Bundle Resource
#         base_path = sys._MEIPASS
#     else:
#         base_path = os.path.abspath(os.getcwd())
#     return os.path.join(base_path)


def add_text_to_allure(filepath,name):
    filebytes = ''
    with open(filepath, 'rb') as file:
        filebytes = file.read()
    allure.attach(filebytes,name,
                  attachment_type=allure.attachment_type.TEXT)

def getphonelist():
    """ 获取手机设备"""
    cmd = r'adb devices'  # % apk_file
    pr = Popen(cmd, stdout=PIPE, shell=True)
    pr.wait()  # 不会马上返回输出的命令，需要等待
    out = pr.stdout.readlines()  # out = pr.stdout.read().decode("UTF-8")
    devices = []
    for i in (out)[1:-1]:
        device = str(i).split("\\")[0].split("'")[-1]
        devices.append(device)
    return devices


def get_test_file():
    """取得测试文件和测试次数，是所有还是单个文件
    """
    case_file_list = {
        'call': 'test_call.py',
        'contact': 'test_contact.py',
        'message': 'test_message.py',
        'chrome': 'test_chrome.py',
    }

    test_count = project_conf.TEST_COUNT
    logging.info('Test App is %s' % project_conf.TEST_APP)
    logging.info('Test Count is %s' % test_count)

    if project_conf.TEST_APP == 'all':
        case_path = os.path.join(
            project_conf.PROJECT_PATH,
            'testcase')
    else:
        case_path = os.path.join(
            project_conf.PROJECT_PATH,
            'testcase',
            case_file_list.get(project_conf.TEST_APP))

    # logging.info('testcase path is %s' % case_path)

    return case_path, test_count


def get_report_path():
    """取得测试报告的路径"""

    allure_path = os.path.join(project_conf.REPORT_DIR,
                               '%s_allure_results' % project_conf.PROJECT_SN)
    allure_report_path = os.path.join(project_conf.REPORT_DIR,
                                      '%s_report' % project_conf.PROJECT_SN)

    if not os.path.exists(allure_path):
        os.makedirs(allure_path)
    if not os.path.exists(allure_report_path):
        os.makedirs(allure_report_path)
    logging.info('Report Path is %s' % allure_report_path)
    return allure_path, allure_report_path


def monitor_logcat(device):
    """监控logcat"""
    logging.info('start logcat monitor')
    logcat = subprocess.Popen('adb logcat -v time',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    base.path_exit(project_conf.ANDROID_LOG_PATH)
    log_path = os.path.join(project_conf.ANDROID_LOG_PATH,
                            '%s_%s_crash_logcat.log' %
                            (get_local_time(), device)
                            )
    pic_path = os.path.join(project_conf.SCREENSHOT_DIR,
                            'crash_%s_%s.png' %
                            (get_local_time(),device))
    while True:
        s = logcat.stdout.readline()
        if ' ANR ' in str(s) or ' Fatal ' in str(s):
            os.system('adb exec-out screencap -p > %s'%pic_path)
            base.add_picture_to_report(pic_path)
            os.system('adb logcat -d > %s' % log_path, )
            add_text_to_allure(log_path,'crash_log')
            logging.critical('Found ANR or Fatal,log was save to %s' %
                             log_path)
            assert False


def monitor_adb(device):
    '监控adb,断开就截图'
    logging.info('start adb monitor')
    base.path_exit(project_conf.ANDROID_LOG_PATH)
    for event in adb.track_devices():
        if not event.present:
            log_path = os.path.join(project_conf.ANDROID_LOG_PATH,
                                    '%s_%s_adb disconnect_logcat.log' %
                                    (get_local_time(),device)
                                    )
            pic_path = os.path.join(project_conf.SCREENSHOT_DIR,
                                    'crash_%s_%s.png' %
                                    (get_local_time(), device))
            os.system('adb exec-out screencap -p > %s'%pic_path)
            base.add_picture_to_report(pic_path)
            os.system('adb logcat -d > %s' % log_path)
            add_text_to_allure(log_path, 'adb disconnect path')
            logging.exception('adb disconnect,log was save to %s' %
                              log_path)
            assert False
        # (event.present,event.serial,event.status)


def m_run(case_path, allure_path, test_count, allure_report_path):
    pytest.main(['-v',
                 '-s',
                 case_path,
                 '--alluredir=%s' % allure_path,
                 '--count=%d' % test_count,
                 '--repeat-scope=function',
                 '--disable-warnings',
                 '--capture=no',
                 ])
    # os.system("pytest -v -s %s --alluredir=%s --count=%d --repeat-scope=function" %
    #           (case_path, allure_path, test_count))
    os.system('allure generate %s -o %s --clean' %
              (allure_path, allure_report_path))


def start_moitor():
    """开启线程监控，闪退，崩溃，重启等"""
    adb_thread = Thread(target=monitor_adb, args=(project_conf.PROJECT_SN,))
    adb_thread.setDaemon(True)
    adb_thread.start()
    logcat_thread = Thread(target=monitor_logcat, args=(project_conf.PROJECT_SN,))
    logcat_thread.setDaemon(True)
    logcat_thread.start()


def run_config(device, app, count, log_name, ):
    """脚本脚本运行流程及配置"""
    project_conf.TEST_LOG_PATH = log_name

    mylog.start_log()
    os.system('adb logcat -c')
    # 开启logcat监控，出现ANR和FAtal就截图保存Log
    start_moitor()
    project_conf.PROJECT_SN = device
    project_conf.TEST_COUNT = count
    project_conf.TEST_APP = app
    # logging.info('main_path is %s ' % project_conf.PROJECT_PATH)
    case_path, test_count = get_test_file()
    allure_path, allure_report_path = get_report_path()
    logging.info('device is %s' % project_conf.PROJECT_SN)
    logging.info('Start Smoking Test')
    m_run(case_path, allure_path, test_count, allure_report_path)
    logging.info('Finished Smoking Test，Sending Email...')
    # myemail.mySendMail()
    logging.info('Mail has been sent')


def get_local_time():
    tformat = '%Y_%m_%d_%H%M%S'
    mytime = time.strftime(tformat, time.localtime())
    return mytime


def get_testlog_path(device):
    """创建测试运行log文件，供Text控件实时读取,运行在主进程"""
    log_path = os.path.join(os.getcwd(),
                            'test_log')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file_name = os.path.join(log_path,
                                 '%s_%s_log.log' %
                                 (get_local_time(), device))
    f = open(log_file_name, 'w', encoding='utf-8')
    f.flush()
    f.close()
    return log_file_name


# 全局进程，用于停止进程后不退出UI界面，只结束进程
test_process = None


def main(app, count):
    devices = getphonelist()
    global test_process
    # 每一次需要清空进程列表，否则出无法启动进程两次的错误
    test_process = []
    for i in devices:
        project_conf.TEST_LOG_PATH = get_testlog_path(i)
        i = Process(target=run_config,
                    args=(i, app, count,
                          project_conf.TEST_LOG_PATH,
                          ))
        test_process.append(i)
    for i in test_process:
        i.start()


def stop():
    # 停止测试进程
    for i in test_process:
        try:
            i.kill()
            logging.info('test is stoped')
        except AttributeError:
            logging.info('please start a test')


if __name__ == '__main__':
    myui.m_window().main_window()
    # mylog.start_log()
    # pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_chrome.py'
    #              r'::TestCase_Chrome::test_open_baidu',
    #              ])
