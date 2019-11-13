from page.pagebase import pBase
import logging
from runlog import testLog


class contact(pBase):
    """联系人应用的所有页面操作类,此类中的d可以直接使用u2的所有方法"""

    def __init__(self):
        self.d = super().mconnect()
        # 包名
        self.packagename = 'com.android.contacts'
        # 添加按钮ID
        self.addbt = "com.android.contacts:id/floating_action_button_container"
        # 联系人名称
        self.contact_name = 'test123'
        # 电话号码
        self.phonenumber = '10086'
        # 联系人名称输入框text
        self.name_input = 'First name'
        # 电话号码输入框text
        self.phone_input = 'Phone'
        # 保存按钮ID
        self.saveid = "com.android.contacts:id/editor_menu_save_button"
        # 保存后的电话号码元素id
        self.saved_phone_number = 'com.android.contacts:id/header'
        # 联系人为空时的提示
        self.emptytext = 'Your contacts list is empty'

    def click_add_bt(self):
        self.mclick(resourceId=self.addbt)

    def input_contact_name(self):
        # d = self.d
        # d.press('home')
        # self.mapp_start(self.packagename)
        self.minput(self.contact_name, text=self.name_input)
        self.minput(self.phonenumber, text=self.phone_input)

    def save_contact(self):
        self.mclick(resourceId=self.saveid)
        logging.info('save success')
        # save = d(resourceId=self.saved_phone_number).get_text()
        # print(save)
        # assert '123' in save

    def get_Verify_text(self):
        # try:
        return self.d(resourceId=self.saved_phone_number).get_text()
        # except Exception as e:
        #     logging.error(e)

    def isempty(self):
        """判断是否有联系人"""
        return self.d(text=self.emptytext).exists

if __name__ == "__main__":
    testLog.startLog()
    tc = contact()
    # tc.mapp_start(tc.packagename)
    # tc.click_add_bt()
    # tc.input_contact_name()
    # tc.save_contact()
    tc.get_Verify_text()
    logging.info('done')
