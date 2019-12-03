import pytest

from page.base import Base
import mylog
from page.message_page import Message
import logging

from mylog import get_log


class TestCase_Message():
    """信息应用测试类"""

    def setup_class(self):
        self.tc = Message()
        self.tc.m_connect()

    def setup(self):
        self.tc.m_app_start(self.tc.mesg_info['packagename'])

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

    @pytest.mark.skip()
    @pytest.mark.parametrize('s_meun,t_meun',
                             Base().m_get_meun('message.yaml'))
    def test_message_meun(self, s_meun, t_meun):
        """测试遍历菜单"""
        self.tc.click_setting()
        self.tc.m_click(text=s_meun)
        if s_meun == 'Hear outgoing message sounds':
            logging.info('on/off bt')
        else:
            t = self.tc.m_get_ele_text(text=t_meun)
            self.tc.m_click_back()
            assert t in t_meun

    def teardown(self):
        self.tc.m_app_stop(self.tc.mesg_info['packagename'])


if __name__ == "__main__":
    mylog.start_log()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_message.py::'
                 r'TestCase_Message::test_meun'])
