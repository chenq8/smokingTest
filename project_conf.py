import os

# 项目主目录
PROJECT_PATH = os.getcwd()
# 设备SN号
PROJECT_SN = ''
# 测试的APP
TEST_APP = ''
# 测试次数
TEST_COUNT = ''
# 测试报告路径
REPORT_DIR = os.path.join(PROJECT_PATH, 'report')
# 失败截图路径
SCREENSHOT_DIR = os.path.join(PROJECT_PATH, 'failpicture')
# 测试Log路径,程序运行后，由主进程传入路径
TEST_LOG_PATH = ''
# android log保存路径
ANDROID_LOG_PATH = os.path.join(PROJECT_PATH,'android_log')