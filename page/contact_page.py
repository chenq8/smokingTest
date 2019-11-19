from page.base import Base
import logging
from runlog import testLog



class Contact(Base):
    """联系人应用的所有页面操作类,此类中的d可以直接使用u2的所有方法"""

    def __init__(self):
        self.contact_info = self.get_data('contact.yaml')

    def click_add_bt(self):
        """点出联系人新建按钮"""
        self.mclick(resourceId=self.contact_info['addbt'])

    def click_meun_bt(self):
        """点击主菜单"""
        self.mclick(description=self.contact_info['meun'])

    def longclick_frist_contact(self):
        """长按第一个联系人"""
        logging.info('long click')
        self.mlong_click(className=self.contact_info['contact_list'],
                         index=3)

    def input_contact_mesg(self):
        """输入联系人姓名及号码"""
        self.minput(self.contact_info['contact_name'],
                    text=self.contact_info['name_input'])
        self.minput(self.contact_info['phonenumber'],
                    text=self.contact_info['phone_input'])

    def save_contact(self):
        """点击联系人保存按钮"""
        self.mclick(resourceId=self.contact_info['saveid'])
        logging.info('save success')

    # def get_Verify_text(self):
    #     """取得控件信息"""
    #     # try:
    #     return self.d(resourceId=self.contact_info['saved_phone_number'])\
    #         .get_text()
    #     # except Exception as e:
    #     #     logging.error(e)

    def contact_isempty(self):
        """判断是否有联系人"""
        return self.d(text=self.contact_info['emptytext']).exists

    def do_del(self):
        """删除操作
        点击删除按钮-确认删除"""
        self.mclick(resourceId=self.contact_info['delbt'])
        self.mclick(resourceId=self.contact_info['do_del'])

    def new_contact(self):
        """新建联系人
        点击添加按钮-输入信息-点击保存"""
        self.click_add_bt()
        self.input_contact_mesg()
        self.save_contact()
        self.mclick_back()

    def click_setting(self):
        self.mclick(resourceId=self.contact_info['setting_id'])