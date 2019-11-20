import pytest

from page.base import Base
from runlog import testLog
from page.message_page import Message
import logging

from runlog.testLog import get_log


class TestCase_Message():
    """信息应用测试类"""

    def setup_class(self):
        self.tc = Message()
        self.tc.mconnect()

    def setup(self):
        # self.tc.mclick_home()
        self.tc.mapp_start(self.tc.mesg_info['packagename'])

    @get_log
    def test_new_sms(self):
        """新建信息
        点击新建-输入号码-输入内容-发送"""
        self.tc.click_create_bt()
        self.tc.input_number()
        self.tc.input_context()
        self.tc.send()

    @get_log
    def test_forward_sms(self):
        """转发信息
        判断列表中是否有信息（无则判断失败）-点击第一个会话-长按第一条信息
        -点击菜单-选择转发-选择新信息-输入号码-发送"""
        if self.tc.mesg_exists():
            self.tc.select_mesg()
            self.tc.click_option()
            self.tc.forward_to_new()
            self.tc.input_number()
            self.tc.send()
        else:
            logging.error('no messages')
            assert False

    @get_log
    def test_new_mms(self):
        """新建彩信
        点击新建-输入号码-输入内容-添加照片-发送"""
        self.tc.click_create_bt()
        self.tc.input_number()
        self.tc.input_context()
        self.tc.attach_photo()
        self.tc.send()

    @get_log
    @pytest.mark.parametrize('s_meun,t_meun',
                             Base().get_meun_data('message.yaml'))
    def test_meun(self,s_meun,t_meun):
        """测试遍历菜单"""
        self.tc.click_setting()
        self.tc.mclick(text=s_meun)
        if s_meun == 'Hear outgoing message sounds':
            logging.info('on/off bt')
        else:
            t = self.tc.get_ele_text(text=t_meun)
            assert t in t_meun
        self.tc.mclick_back()

    def teardown(self):
        self.tc.mapp_stop(self.tc.mesg_info['packagename'])


if __name__ == "__main__":
    testLog.startLog()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_message.py::'
                 r'TestCase_Message::test_meun'])
