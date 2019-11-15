import pytest
from runlog import testLog
from page.contact_app import Contact
import logging


class TestCase_contact():
    """联系人应用测试类，只可以使用contact类中的方法"""

    def setup_class(self):
        self.tc = Contact()
        self.tc.mconnect()


    def setup(self):
        self.tc.mapp_start(self.tc.contact_info['packagename'])

    def test_new_contact(self):
        """测试新建联系人"""
        tc = self.tc
        tc.new_contact()
        # savednumber = tc.get_Verify_text()
        # logging.info('savednumber is %s ' % savednumber)
        # assert '10086' in savednumber

    def test_del_contact(self):
        """测试删除联系人"""
        tc = self.tc
        if tc.contact_isempty():
            tc.new_contact()
            tc.del_contact()
        else:
            tc.del_contact()

    def test_meun(self):
        """测试遍历菜单"""
        self.tc.click_all_meun()

    def teardown(self):
        # self.tc.mapp_stop(self.tc.contact_info['packagename'])
        self.tc.mapp_stop_all()
        print('执行完成')


if __name__ == "__main__":
    testLog.startLog()
    pytest.main([r'D:\mytools\SmokingTestCase\testcase\test_contact.py'])
