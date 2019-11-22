import pytest

from page.base import Base
from runlog import testLog
from page.call_page import Call
from runlog.testLog import get_log


class TestCase_Call():
    """联系人应用测试类，只可以使用contact类中的方法"""
    def setup_class(self):
        self.tc = Call()
        self.tc.m_connect()

    def setup(self):
        self.tc.m_app_start(self.tc.call_info['packagename'])

    @get_log
    def test_make_call(self):
        """拨打电话"""
        if self.tc.contact_notexsits():
            self.tc.create_contact()
            self.tc.click_call_bt()
        else:
            self.tc.click_contact()
            self.tc.click_call_bt()
        self.tc.end_call()

    @pytest.mark.parametrize('s_meun,t_meun',
                             Base().m_get_meun('call.yaml'))
    @get_log
    def test_meun(self,s_meun,t_meun):
        """测试遍历菜单"""
        self.tc.click_meun()
        self.tc.click_setting()
        self.tc.m_click(text=s_meun)
        t = self.tc.m_get_ele_text(t_meun)
        assert t in t_meun

    def teardown(self):
        self.tc.m_app_stop(self.tc.call_info['packagename'])
        print('Finished test')


if __name__ == "__main__":
    testLog.startLog()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_call.py::TestCase_Call::test_make_call',
                 ])
