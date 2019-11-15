import pytest
from runlog import testLog
from page.message_page import Message
import logging


class TestCase_Message():
    """信息应用测试类"""

    def setup_class(self):
        self.tc = Message()
        self.tc.mconnect()

    def setup(self):
        self.tc.mapp_start(self.tc.mesg_info['packagename'])

    def test_new_sms(self):
        self.tc.new_sms()

    data=Message().get_data('call.yaml')
    meun_data = [(x,y) for x,y in
        zip(data['secondary_meun'],data['third_meun'])]

    @pytest.mark.parametrize('s_meun,t_meun',meun_data)
    def test_meun(self,s_meun,t_meun):
        """测试遍历菜单"""
        self.tc.click_all_meun(s_meun,t_meun)

    def teardown(self):
        self.tc.mapp_stop(self.tc.mesg_info['packagename'])
        print('执行完成')


if __name__ == "__main__":
    testLog.startLog()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_call.py::TestCase_Call::test_meun'])
