import pytest
from runlog import testLog
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


def main(devices):
    """脚本程序入口"""
    testLog.startLog()
    project_conf.PROJECT_SN = devices

    case_path = os.path.join(project_conf.PROJECT_PATH,'testcase','test_contact.py')
    allure_path = os.path.join(project_conf.PROJECT_PATH,'report','%s_allure_results'%project_conf.PROJECT_SN)
    allure_report_path = os.path.join(project_conf.PROJECT_PATH,'report','%s_report'%project_conf.PROJECT_SN)

    if not os.path.exists(allure_path):
        os.makedirs(allure_path)
    if not os.path.exists(allure_report_path):
        os.makedirs(allure_report_path)

    logging.info('device is %s'%project_conf.PROJECT_SN)
    logging.info('Start smoking test')

    pytest.main(['-v', '-s',case_path, '--alluredir=%s' % allure_path])
    logging.info('allure is %s report is %s'%(allure_path,allure_report_path))
    os.system('allure generate %s -o %s --clean' %
              (allure_path, allure_report_path))

    logging.info('Finished smoking test')


if __name__ == '__main__':
    p = []
    devices = getphonelist()
    for i in devices:
        i = Process(target=main,args=(i,))
        p.append(i)
    for i in p:
        i.start()
    for i in p:
        i.join()