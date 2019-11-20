import pytest

from page.base import Base
from runlog import testLog
from page.contact_page import Contact
import logging

from runlog.testLog import get_log


class TestCase_contact():
    """联系人应用测试类，只可以使用contact类中的方法"""

    def setup_class(self):
        self.tc = Contact()
        self.d = self.tc.mconnect()

    def setup(self):
        self.tc.mapp_start(self.tc.contact_info['packagename'])

    # @get_log
    # def test_new_contact(self):
    #     """测试新建联系人
    #     点击添加按钮-输入信息-点击保存"""
    #     self.tc.click_add_bt()
    #     self.tc.input_contact_mesg()
    #     self.tc.save_contact()
    #
    # @get_log
    # def test_del_contact(self):
    #     """测试删除联系人
    #     如果无联系人，则新建后再删除"""
    #     tc = self.tc
    #     if tc.contact_isempty():
    #         tc.new_contact()
    #         tc.longclick_frist_contact()
    #         tc.do_del()
    #     else:
    #         tc.longclick_frist_contact()
    #         tc.do_del()

    @pytest.mark.parametrize('s_meun,t_meun',
                             Base().get_meun_data('contact.yaml'))
    def test_meun(self, s_meun, t_meun):
        """遍历一二级菜单
               后续需要优化
               点击菜单-点击设置-点击二级菜单列表-返回-重启APP"""
        # 开始遍历
        self.tc.click_meun_bt()
        self.tc.click_setting()
        self.tc.mclick(text=s_meun)
        t = self.tc.get_ele_text(text=t_meun)
        if s_meun is 'My info':
            self.tc.mclick_back()
            self.tc.mclick_back()
        # elif s_meun is 'Blocked numbers':
        #     self.tc.mclick_back()
        #     # self.mclick(className=self.contact_info['block_number'])
        #     # self.tc.mapp_stop('com.android.server.telecom')
        else:
            self.tc.mclick_back()
        assert t in t_meun

    def teardown(self):
        self.tc.mapp_stop(self.tc.contact_info['packagename'])


if __name__ == "__main__":
    testLog.startLog()
    pytest.main(['-q', r'D:\mytools\SmokingTestCase\testcase\test_contact.py'])
