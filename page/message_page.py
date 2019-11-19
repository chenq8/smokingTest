from page.base import Base
import logging


class Message(Base):

    def __init__(self):
        """取得配置信息"""
        self.mesg_info = self.get_data('message.yaml')

    def click_create_bt(self):
        """"点击新建按钮"""
        self.mclick(resourceId=self.mesg_info['new_chat'])

    def input_number(self):
        """"输入号码"""
        self.minput(self.mesg_info['number'], className=self.mesg_info['number_in'])
        self.d.send_action('go')

    def input_context(self):
        """输入信息内容"""
        self.minput(self.mesg_info['mesg_text'], text=self.mesg_info['message'])

    def attach_photo(self):
        """为信息添加照片"""
        self.mclick(resourceId=self.mesg_info['attach_bt'])
        self.mclick(text=self.mesg_info['camera'])
        self.mclick(resourceId=self.mesg_info['takept'])

    def send(self):
        """发送按钮"""
        self.mclick(self.mesg_info['send_bt'])

    def click_setting(self):
        """进入信息设置"""
        self.click_option()
        self.mclick(text=self.mesg_info['setting'])

    def mesg_exists(self):
        """判断是否有信息存在"""
        return self.findele(resourceId=self.mesg_info['mesg_list']).exists

    def select_mesg(self):
        """选择要转发的信息"""
        self.mclick(resourceId=self.mesg_info['mesg_list'],
                    index=0)
        self.mlong_click(resourceId=self.mesg_info['session_list'])

    def click_option(self):
        """点击选项菜单，在信息内容列表界面"""
        self.mclick(description=self.mesg_info['option_list'])

    def forward_to_new(self):
        """"选择使用新信息转发
        点击选项菜单-选择转发-选择使用新信息"""
        self.mclick(resourceId=self.mesg_info['forward_bt'], index=1)
        self.mclick(resourceId=self.mesg_info['for_new'])

    def click_all_meun(self, s_meun, t_meun):
        self.click_setting()
        self.mclick(text=s_meun)
        if s_meun == 'Hear outgoing message sounds':
            logging.info('on/off bt')
        else:
            t = self.findele(text=t_meun).get_text()
            assert t in t_meun
