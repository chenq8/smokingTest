from page.base import Base
import logging

from time import sleep


class Message(Base):
    def __init__(self):
        self.mesg_info = self.get_data('meesage.yaml')

    def new_sms(self):
        """新建信息"""
        self.mclick(resourceId=self.mesg_info['new_chat'])
        self.minput(self.mesg_info['number'],self.mesg_info['number_in'])
        self.d.send_action('go')
        self.minput(self.mesg_info['mesg_text'],self.mesg_info['meesage'])
        self.mclick(self.mesg_info['send'])


    def click_all_meun(self,s_meun,t_meun):
        self.mclick(resourceId=self.mesg_info['meun'])
        self.mclick(text=self.mesg_info['setting'])
        self.mclick(text=s_meun)
        t = self.findele(text=t_meun).get_text()
        assert t in t_meun
