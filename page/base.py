import uiautomator2 as u2
import logging
import os
import time
from runlog import testLog
from testdata import mydata


class pBase():
    """页面及元素操作的所有公共方法"""

    def __init__(self):
        self.d = None

    def mconnect(self, *args):
        """连接服务"""

        self.d = u2.connect(*args)
        self.d.click_post_delay = 1.5
        logging.info('connect success')
        return self.d
        #
        # logging.error('connect fail')
        # logging.error(e)

    def mgetinfo(self):
        """取得设备信息"""
        return self.d.info

    def mapp_start(self, packagename):
        """如果应用正在运行，刚停止后运行，如果未运行，则启动"""
    # try:
        if packagename in self.d.app_list_running():
            self.d.app_stop(packagename)
            logging.info('app %s stop done' % packagename)
            self.d.app_start(packagename)
            logging.info('app %s start done' % packagename)
        else:
            self.d.app_start(packagename)
            logging.info('app %s start done' % packagename)
    # except Exception as e:
    #     logging.error(e)


    def mapp_stop(self,packagename):
        """停止应用"""
        self.d.app_stop(packagename)

    def findelement(self, **kwargs):
        """查找控件"""
        self.d(**kwargs)

    def mclick(self, **kwargs):
        """点击操作"""
    # try:
        self.d(**kwargs).click()
        logging.info('Found Element %s' % kwargs)
    # except Exception as e:
    #     logging.error('Not Found Element %s' % kwargs)
    #     logging.error(e)
    #     self.mscreenshot()

    def mlong_click(self, index=None,**kwargs):
        """长按操作,当前版本不支持长按操作，使用滑动到同一个点来实现长按操作"""
        if index is not None:
            logging.info('this index is %s'%index)
            x,y = self.d(**kwargs)[index].center()
            self.d.swipe(x, y, x, y, 2)
            logging.info('Found Element %s' % kwargs)
        else:
            logging.info('no index')
            x, y = self.d(**kwargs).center()
            self.d.swipe(x, y, x, y, 2)
            logging.info('Found Element %s' % kwargs)

            # logging.error('Not Found Element %s' % kwargs)
            # logging.error(e)
            # self.mscreenshot()

    def minput(self, mstring, **kwargs):
    # try:
        self.d(**kwargs).send_keys(mstring)
        logging.info('input mastring %s' % mstring)
    # except Exception as e:
    #     logging.error('input error %s' % mstring)
    #     logging.error(e)
    #     self.mscreenshot()

    def mscreenshot(self):
        """以当前时间命名截图"""
        tformat = '%Y%m%d%H%M%S'
        mytime = time.strftime(tformat, time.localtime())
        filename = os.path.join(r'D:\mytools\SmokingTestCase\failpicture', mytime + '.png')
        try:
            self.d.screenshot(filename)
            logging.info('screenshot success')
        except Exception as e:
            logging.info('screenshot fail')
            logging.error(e)

    def get_data(self,filename):
        """取得APP中所有操作数据"""
        data = mydata.MyData()
        path = os.path.join(os.path.split(os.getcwd())[0],'testdata',filename)
        return data.load_data(path)

if __name__ == '__main__':
    testLog.startLog()
    m = pBase()
    m.mconnect()
    # m.sclick(text='Settings')
    logging.info(m.d(text='Settings').info)
    logging.info(m.d.service("uiautomator").stop())
    logging.info('done')
