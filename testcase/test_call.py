import pytest
from runlog import testLog
from page.call_app import Call
import logging


class TestCase_contact():
    """联系人应用测试类，只可以使用contact类中的方法"""

    def setup_class(self):
        self.tc = Call()
        self.tc.mconnect()

    def setup(self):
        self.tc.mapp_start(self.tc.call_info['packagename'])

    def test_make_call(self):
        self.tc.make_call()
        self.tc.end_call()

    #
    # def test_meun(self):
    #     """测试遍历菜单"""
    #     self.tc.click_all_meun()

    def teardown(self):
        self.tc.mapp_stop(self.tc.call_info['packagename'])
        print('执行完成')


if __name__ == "__main__":
    testLog.startLog()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_call.py'])
