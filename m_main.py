import pytest
import MyLog
import os
import logging
import project_conf
from multiprocessing import Process
import subprocess


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
        'caontact': 'test_contact.py',
        'message': 'test_message.py',
        'chrome': 'test_chrome.py',
    }

    test_app = project_conf.TEST_APP
    test_count = project_conf.TEST_COUNT

    if test_app == 'all':
        case_path = os.path.join(project_conf.PROJECT_PATH, 'testcase')
    else:
        case_path = os.path.join(project_conf.PROJECT_PATH,
                                 'testcase',
                                 case_file_list.get(test_app))

    logging.info('test app is %s' % test_app)
    logging.info('test count is %s' % test_count)
    logging.info('testcase path is %s' % case_path)

    return case_path, test_count


def get_report_path():
    """取得测试报告的路径"""
    allure_path = os.path.join(project_conf.PROJECT_PATH,
                               'report',
                               '%s_allure_results' % project_conf.PROJECT_SN)
    allure_report_path = os.path.join(project_conf.PROJECT_PATH,
                                      'report',
                                      '%s_report' % project_conf.PROJECT_SN)

    if not os.path.exists(allure_path):
        os.makedirs(allure_path)
    if not os.path.exists(allure_report_path):
        os.makedirs(allure_report_path)

    logging.info('allure_results is %s' % allure_path)
    logging.info('report path is %s' % allure_report_path)
    return allure_path, allure_report_path


def run_config(devices):
    """脚本脚本运行流程及配置"""
    project_conf.PROJECT_SN = devices
    MyLog.startLog()
    case_path, test_count = get_test_file()

    allure_path, allure_report_path = get_report_path()

    logging.info('device is %s' % project_conf.PROJECT_SN)
    logging.info('Start smoking test')
    pytest.main(['-v',
                 '-s',
                 case_path,
                 '--alluredir=%s' % allure_path,
                 '--count=%d' % test_count,
                 '--repeat-scope=function'])
    os.system('allure generate %s -o %s --clean' %
              (allure_path, allure_report_path))

    logging.info('Finished smoking test')
    # myemail.mySendMail()
    # logging.info('Mail has been sent')


def main():
    p = []
    devices = getphonelist()
    for i in devices:
        i = Process(target=run_config, args=(i,))
        p.append(i)
    for i in p:
        i.start()

    # 此处不能加join，否则gui会无响应
    # for i in p:
    #     i.join()

# def go():
#     p = Process(target=main)
#     p.start()
