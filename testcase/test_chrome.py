import pytest

from page.base import Base
from runlog import testLog
from page.chrome_page import Chrome

from runlog.testLog import get_log


class TestCase_Chrome():
    """联系人应用测试类，只可以使用contact类中的方法"""

    def setup_class(self):
        self.tc = Chrome()
        self.tc.mconnect()

    def setup(self):
        # self.tc.mapp_start(self.tc.chrome_info['packagename'])
        self.tc.start_chrome()

    @get_log
    def test_open_baidu(self):
        self.tc.input_url("www.baidu.com")
        assert '百度一下' in self.tc.get_baidu_text

    @pytest.mark.parametrize('s_meun,t_meun',
                             Base().get_meun_data('chrome.yaml'))
    @get_log
    def test_meun(self,s_meun,t_meun):
        """测试遍历菜单"""
        self.tc.click_meun()
        self.tc.click_setting()
        self.tc.mclick(text=s_meun)
        t = self.tc.get_ele_text(t_meun)
        self.tc.mclick_back()
        assert t in t_meun

    def teardown(self):
        self.tc.mapp_stop(self.tc.chrome_info['packagename'])


if __name__ == "__main__":
    testLog.startLog()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_chrome.py'
                 r'::TestCase_Chrome::test_open_baidu',
                 ])
