import pytest
from page.base import Base
from MyLog import *
from page.chrome_page import Chrome

class TestCase_Chrome():
    """联系人应用测试类，只可以使用contact类中的方法"""

    def setup_class(self):
        self.tc = Chrome()
        self.tc.m_connect()

    def setup(self):
        # self.tc.mapp_start(self.tc.chrome_info['packagename'])
        self.tc.start_chrome()

    @get_log
    def test_open_baidu(self):
        self.tc.input_url("www.baidu.com")
        assert '百度一下' in self.tc.get_baidu_text()

    @pytest.mark.skip()
    @pytest.mark.parametrize('s_meun,t_meun',
                             Base().m_get_meun('chrome.yaml'))
    def test_chrome_meun(self,s_meun,t_meun):
        """测试遍历菜单"""
        self.tc.click_meun()
        self.tc.click_setting()
        self.tc.m_click(text=s_meun)
        t = self.tc.m_get_ele_text(text=t_meun)
        self.tc.m_click_back()
        assert t in t_meun

    def teardown(self):
        self.tc.m_app_stop(self.tc.chrome_info['packagename'])


if __name__ == "__main__":
    startLog()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_chrome.py'
                 r'::TestCase_Chrome::test_open_baidu',
                 ])
