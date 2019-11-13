import pytest
from runlog import testLog
from page.contact_app import contact
import logging


class TestCase_call():
    """联系人应用测试类，只可以使用contact类中的方法"""

    def setup_class(self):
        self.tc = contact()
        logging.info(type(self.tc))

    def test_new_contact(self):
        """测试新建联系人"""
        tc = self.tc

        tc.mapp_start(tc.packagename)
        tc.click_add_bt()
        tc.input_contact_name()
        tc.save_contact()
        savednumber = tc.get_Verify_text()
        logging.info('savednumber is %s ' % savednumber)
        assert '10086' in savednumber

    def teardown_class(self):
        # self.driver.app_stop('com.android.contacts')
        # self.driver.app_stop('com.android.dialer')
        logging.info(self.tc.mgetinfo())
        print('执行完成')


if __name__ == "__main__":
    testLog.startLog()
    pytest.main(['-q', r'D:\mytools\SmokingTestCase\testcase\test_call.py'])
