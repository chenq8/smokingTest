import uiautomator2 as u2
import logging
import os
import time
from runlog import testLog
import yaml


class Base():
    """页面及元素操作的所有公共方法"""

    def __init__(self):
        self.d = None

    def mconnect(self, *args):
        """连接服务"""

        try:
            self.d = u2.connect(*args)
            self.d.click_post_delay = 1.5
            self.d.set_fastinput_ime(False)
            logging.info('connect success')
            return self.d
        except Exception as e:
            logging.error(e)
            logging.error('connect fail')

    def mget_info(self):
        """取得设备信息"""
        return self.d.info

    def mclick_home(self):
        """点击home键"""
        self.d.press('home')

    def mclick_back(self):
        self.d.press('back')

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

    def mapp_stop(self, packagename):
        """停止应用"""
        self.d.app_stop(packagename)

    def mapp_stop_all(self, **kwargs):
        """停止所有应用"""
        self.d.app_stop_all(**kwargs)

    def findele(self, **kwargs):
        """查找控件"""
        return self.d(**kwargs)

    def get_ele_text(self,ele):
        """返回控件文本"""
        return self.findele(text=ele).get_text()

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
            logging.error('Not Found Element %s' % kwargs)
            logging.error(e)
            self.mscreenshot()

    def mlong_click(self, index=None, **kwargs):
        """长按操作,当前版本不支持长按操作，使用滑动到同一个点来实现长按操作"""
        try:
            if index is not None:
                x, y = self.d(**kwargs)[index].center()
                self.d.swipe(x, y, x, y, 2)
                logging.info('clicked Element %s[%d]' % (kwargs, index))
            else:
                x, y = self.d(**kwargs).center()
                self.d.swipe(x, y, x, y, 2)
                logging.info('longclicked Element %s' % kwargs)
        except Exception as e:
            logging.error(e)
            logging.error('Not Found Element %s' % kwargs)
            self.mscreenshot()

    def input_enter(self):
        self.d.send_action('search')

    def minput(self, mstring, **kwargs):
        """控件输入，mstring为输入的内容，**kwargs为控件查找方式"""
        try:
            self.d(**kwargs).send_keys(mstring)
            logging.info('input mastring %s' % mstring)
        except Exception as e:
            logging.error(e)
            logging.error('input error %s' % mstring)
            self.mscreenshot()

    def mscreenshot(self):
        """以当前时间命名截图"""
        tformat = '%Y%m%d%H%M%S'
        mytime = time.strftime(tformat, time.localtime())
        filename = os.path.join(os.path.split(os.getcwd())[0],
                                'failpicture', mytime + '.png')
        try:
            self.d.screenshot(filename)
            logging.info('screenshot success')
        except Exception as e:
            logging.error(e)
            logging.info('screenshot fail')

    def get_data(self, filename):
        """取得APP中配置文件中操作数据"""
        path = os.path.join(os.path.split(os.getcwd())[0],
                            'testdata',
                            filename)
        with open(path, 'r',
                  encoding='utf-8') as file:
            files = file.read()
        return yaml.load(files, Loader=yaml.SafeLoader)

    def get_meun_data(self,filename):
        data = self.get_data(filename)
        meun_data = [(x, y) for x, y in
                     zip(data['secondary_meun'], data['third_meun'])]
        return meun_data

    def scroll_to_end(self):
        """滚至最后"""
        self.d(scrollable=True).scroll.toEnd()