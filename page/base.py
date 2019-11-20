import uiautomator2 as u2
from runlog import testLog
import logging
import os
import time
import yaml
import sys
import allure
import uuid

class Base():
    """页面及元素操作的所有公共方法"""

    def __init__(self):
        self.d = None

    def mconnect(self, *args):
        """连接服务"""
        try:
            self.d = u2.connect(*args)
            self.d.click_post_delay = 1.5
            self.d.implicitly_wait(5)
            logging.info('connect success')
            return self.d
        except Exception as e:
            logging.error(e)
            logging.error('connect fail')

    def mget_info(self):
        """取得设备信息"""
        return self.d.info

    def input_enter(self):
        """输入完成后，直接搜索，模拟输入法搜索"""
        self.d.send_action('search')
        logging.info('clicked search')

    def mclick_home(self):
        """点击home键"""
        self.d.press('home')
        logging.info('clicked home')

    def mclick_back(self):
        """返回键"""
        self.d.press('back')
        logging.info('clicked back')

    def mapp_start(self, packagename):
        """如果应用正在运行，刚停止后运行，如果未运行，则启动"""
        try:
            self.mclick_home()
            if packagename in self.d.app_list_running():
                self.d.app_stop(packagename)
                logging.info('app %s stop done' % packagename)
                self.d.app_start(packagename)
                logging.info('app %s start done' % packagename)
            else:
                self.d.app_start(packagename)
                logging.info('app %s start done' % packagename)
        except Exception as e:
            logging.error(e)
            logging.error("APP %s start fial" % packagename)
            name = sys._getframe(1).f_code.co_name
            self.mscreenshot(name)

    def mapp_stop(self, packagename):
        """停止应用"""
        self.d.app_stop(packagename)

    def mapp_stop_all(self, **kwargs):
        """停止所有应用"""
        self.d.app_stop_all(**kwargs)

    def findele(self, **kwargs):
        """查找控件"""
        try:
            ele = self.d(**kwargs)
            return ele
        except Exception as e:
            logging.error(e)
            logging.error('Not Found Element %s' % kwargs)
            name = sys._getframe(1).f_code.co_name
            self.mscreenshot(name)
            assert False,'can not found element'

    def get_ele_text(self,**kwargs):
        """返回控件文本"""
        try:
            return self.d(**kwargs).get_text()
        except:
            logging.error(e)
            logging.error('Not Found Element %s' % kwargs)
            name = sys._getframe(1).f_code.co_name
            self.mscreenshot(name)
            assert False, 'can not found element'

    def ele_exists(self,**kwargs):
        """"判断控件是否存在"""
        return self.d.exists(**kwargs)

    def mclick(self, index=None, **kwargs):
        """点击操作"""
        try:
            if index is not None:
                self.d(**kwargs)[index].click()
                logging.info('clicked Element %s[%d]' % (kwargs, index))
            else:
                self.d(**kwargs).click()
                logging.info('clicked Element %s' % kwargs)
        except Exception as e:
            logging.error(e)
            logging.error('Not Found Element %s' % kwargs)
            name = sys._getframe(1).f_code.co_name
            self.mscreenshot(name)
            assert False,'can not found element'

    def mlong_click(self, index=None, **kwargs):
        """长按操作,当前版本不支持长按操作，使用滑动到同一个点来实现长按操作"""
        try:
            if index is not None:
                x, y = self.d(**kwargs)[index].center()
                self.d.swipe(x, y, x, y, 2)
                logging.info('long clicked Element %s[%d]' % (kwargs, index))
            else:
                x, y = self.d(**kwargs).center()
                self.d.swipe(x, y, x, y, 2)
                logging.info('long clicked Element %s'%kwargs)
        except Exception as e:
            logging.error(e)
            logging.error('Not Found Element %s'% kwargs)
            name = sys._getframe(1).f_code.co_name
            self.mscreenshot(name)
            assert False,'can not found element'

    def minput(self, mstring, **kwargs):
        """控件输入，mstring为输入的内容，**kwargs为控件查找方式"""
        try:
            self.d(**kwargs).send_keys(mstring)
            logging.info('input mstring %s' % mstring)
        except Exception as e:
            logging.error(e)
            logging.error('input error %s' % mstring)
            name = sys._getframe(1).f_code.co_name
            self.mscreenshot(name)
            assert False,'can not find element'

    def mscreenshot(self,name):
        """以当前时间+调用函数名命名截图"""
        tformat = '%Y_%m_%d_%H%M%S'
        mytime = time.strftime(tformat, time.localtime())
        filename = '%s_%s_.png'%(mytime,name)
        logging.info('fail picture name is %s'%filename)
        filepath = os.path.join(r'D:\mytools\SmokingTestCase',
                                'failpicture',
                                filename)
        filebytes = ''
        with open(self.d.screenshot(filepath),'rb') as file:
            filebytes = file.read()
        try:
            allure.attach(filebytes,
                          'fail scrennshot',
                          attachment_type=allure.attachment_type.PNG)
            # self.d.screenshot(filepath)
            logging.info('screenshot success')
        except Exception as e:
            logging.error(e)
            logging.info('screenshot fail')

    def get_data(self, filename):
        """取得APP中配置文件中操作数据"""
        # path = os.path.join(os.path.split(os.getcwd())[0],
        #                     'testdata',
        #                     filename)
        path = os.path.join(r'D:\mytools\SmokingTestCase',
                            'testdata',
                            filename)
        with open(path, 'r',encoding='utf-8') as file:
            files = file.read()
        return yaml.load(files, Loader=yaml.SafeLoader)

    def get_meun_data(self,filename):
        """取得各级菜单名称"""
        path = os.path.join(r'D:\mytools\SmokingTestCase',
                            'testdata',
                            filename)
        data = self.get_data(path)
        meun_data = [(x, y) for x, y in
                     zip(data['secondary_meun'], data['third_meun'])]
        return meun_data

    def scroll_to_end(self):
        """滚至最后"""
        self.d(scrollable=True).scroll.toEnd()