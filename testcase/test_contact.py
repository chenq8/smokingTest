import pytest
from runlog import testLog
from page.contact_app import Contact
import logging


class TestCase_contact():
    """联系人应用测试类，只可以使用contact类中的方法"""

    def setup_class(self):
        self.tc = Contact()
        self.d  = self.tc.mconnect()

    def setup(self):
        self.tc.mapp_start(self.tc.contact_info['packagename'])

    # def test_new_contact(self):
    #     """测试新建联系人"""
    #     tc = self.tc
    #     tc.new_contact()
    #     # savednumber = tc.get_Verify_text()
    #     # logging.info('savednumber is %s ' % savednumber)
    #     # assert '10086' in savednumber
    #
    # def test_del_contact(self):
    #     """测试删除联系人"""
    #     tc = self.tc
    #     if tc.contact_isempty():
    #         tc.new_contact()
    #         tc.del_contact()
    #     else:
    #         tc.del_contact()

    data=Contact().get_data('contact.yaml')
    meun_data = [(x,y) for x,y in
        zip(data['secondary_meun'],data['third_meun'])]

    @pytest.mark.parametrize('s_meun,t_meun',meun_data)
    def test_meun(self,s_meun,t_meun):
        """测试遍历菜单"""
        self.tc.click_all_meun(s_meun,t_meun)


    def teardown(self):
        self.tc.mapp_stop(self.tc.contact_info['packagename'])
        self.d.press('home')
        # self.tc.mapp_stop_all()
        print('执行完成')


if __name__ == "__main__":
    testLog.startLog()
    pytest.main(['-q',r'D:\mytools\SmokingTestCase\testcase\test_contact.py'])
