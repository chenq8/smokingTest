from page.base import Base
import logging

from time import sleep


class Call(Base):
    def __init__(self):
        self.call_info = self.get_data('call.yaml')

    def contact_notexsits(self):
        """无联系人则返回TRUE"""
        self.mclick(resourceId=self.call_info['contacts_bt'])
        return self.d(text=self.call_info['no_contact']).exists()

    def create_contact(self):
        """电话应用内创建首个联系人"""
        # ct = Contact()
        self.mclick(resourceId=self.call_info['create_bt'])
        # ct.input_contact_mesg()
        # ct.save_contact()
        self.minput(self.call_info['contact_name'],
                    text=self.call_info['name_input'])
        self.minput(self.call_info['phonenumber'],
                    text=self.call_info['phone_input'])

        self.mclick(resourceId=self.call_info['saveid'])

    def make_call(self):
        """拨打电话"""
        if self.contact_notexsits():
            self.create_contact()
            self.mclick(resourceId=self.call_info['call_bt'])
        else:
            self.mclick(resourceId=self.call_info['contact_list'],
                        index=1)
            self.mclick(resourceId=self.call_info['call_bt'])

    def __get_call_time(self):
        """取得通话时间,模拟器无text时间值"""
        return self.d(resourceId=self.call_info['call_time']).get_text()

    def end_call(self):
        """通话10秒后挂断电话"""
        sleep(10)
        self.mclick(resourceId=self.call_info['end_call'])

    def click_all_meun(self,s_meun,t_meun):
        self.mclick(resourceId=self.call_info['meun'])
        self.mclick(text=self.call_info['setting'])
        self.mclick(text=s_meun)
        t = self.findele(text=t_meun).get_text()

        assert t in t_meun
