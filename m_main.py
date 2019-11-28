import pytest
import os
import logging
import project_conf
from multiprocessing import Process
from threading import Thread, Event
import subprocess
import myui
import MyLog


def getphonelist():
    """ 获取手机设备"""
    cmd = r'adb devices'  # % apk_file
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
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
    logging.info('test app is %s' % project_conf.TEST_APP)
    logging.info('test count is %s' % test_count)

    if project_conf.TEST_APP == 'all':
        case_path = os.path.join(
                                 project_conf.PROJECT_PATH,
                                 'testcase')
    else:
        case_path = os.path.join(
                                 project_conf.PROJECT_PATH,
                                 'testcase',
                                 case_file_list.get(project_conf.TEST_APP))

    logging.info('testcase path is %s' % case_path)

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

    logging.info('allure_results is %s' % allure_path)
    logging.info('report path is %s' % allure_report_path)
    return allure_path, allure_report_path


def run_config(devices, app, count):
    """脚本脚本运行流程及配置"""
    project_conf.PROJECT_SN = devices
    project_conf.TEST_COUNT = count
    project_conf.TEST_APP = app

    case_path, test_count = get_test_file()

    allure_path, allure_report_path = get_report_path()

    logging.info('device is %s' % project_conf.PROJECT_SN)
    logging.info('Start smoking test')
    pytest.main(['-v',
                 '-s',
                 case_path,
                 '--alluredir=%s' % allure_path,
                 '--count=%d' % test_count,
                 '--repeat-scope=function'
                 ])
    os.system('allure generate %s -o %s --clean' %
              (allure_path, allure_report_path))

    logging.info('Finished smoking test')
    # myemail.mySendMail()
    # logging.info('Mail has been sent')


# 全局进程，用于停止进程后不退出UI界面，只结束进程
# test_thread = None


# def main(app, count,):
#     devices = getphonelist()
#     global p
#     # 每一次需要清空进程列表，否则出无法启动进程两次的错误
#     p = []
#     for i in devices:
#         i = Process(target=run_config, args=(i, app, count))
#         p.append(i)
#     for i in p:
#         i.start()
#
#
# def stop():
#     # 停止测试进程
#     for i in p:
#         try:
#             i.kill()
#             logging.info('test is stoped')
#         except AttributeError:
#             logging.info('please start a test')

#使用线程，多开UI界面

def main(app, count,):
    devices = getphonelist()
    global test_thread
    # 每一次需要清空线程列表，否则出无法启动进程两次的错误

    test_thread = Thread(target=run_config, args=(devices[0], app, count))
    #设置为守护线程，当UI退出，则立退终止线程
    test_thread.daemon = True
    test_thread.start()

    # for i in devices:
    #     i = Thread(target=run_config, args=(i, app, count))
    #     p.append(i)
    #     i.setDaemon(True)
    # for i in p:
    #     i.start()

if __name__ == '__main__':
    myui.m_window().main_window()
