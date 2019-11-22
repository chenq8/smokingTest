from page.base import Base


class Call(Base):
    def __init__(self):
        self.call_info = self.m_get_data('call.yaml')

    def contact_notexsits(self):
        """无联系人则返回TRUE"""
        self.m_click(resourceId=self.call_info['contacts_bt'])
        return self.d(text=self.call_info['no_contact']).exists()

    def create_contact(self):
        """电话应用内创建首个联系人"""
        self.m_click(resourceId=self.call_info['create_bt'])
        self.m_input(self.call_info['contact_name'],
                     text=self.call_info['name_input'])
        self.m_input(self.call_info['phonenumber'],
                     text=self.call_info['phone_input'])
        self.m_click(resourceId=self.call_info['saveid'])

    def click_call_bt(self):
        """点击拨号"""
        self.m_click(resourceId=self.call_info['call_bt'])

    def click_contact(self):
        """点击第一个联系人"""
        self.m_click(resourceId=self.call_info['contact_list'],
                     index=1)

    def get_call_time(self):
        """取得通话时间,模拟器无text时间值"""
        return self.d(resourceId=self.call_info['call_time']).get_text()

    def end_call(self):
        """通话10秒后挂断电话"""
        flag = True
        while flag:
            if '00:10' in self.get_call_time():
                self.m_click(resourceId=self.call_info['end_call'])
                flag = False

    def click_meun(self):
        """点击菜单"""
        self.m_click(resourceId=self.call_info['meun'])

    def click_setting(self):
        """点击设置"""
        self.m_click(text=self.call_info['setting'])