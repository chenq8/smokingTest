from page.base import Base
import logging


class Message(Base):

    def __init__(self):
        """取得配置信息"""
        self.mesg_info = self.m_get_data('message.yaml')

    def click_create_bt(self):
        """"点击新建按钮"""
        self.m_click(resourceId=self.mesg_info['new_chat'])
        logging.info('click create bt done')

    def input_number(self):
        """"输入号码"""
        self.m_input(self.mesg_info['number'], className=self.mesg_info['number_in'])
        self.d.send_action('go')
        logging.info('input phone number done')

    def input_context(self):
        """输入信息内容"""
        self.m_input(self.mesg_info['mesg_text'], resourceId=self.mesg_info['message'])
        logging.info('input message context done')

    def attach_photo(self):
        """为信息添加照片"""
        self.m_click(resourceId=self.mesg_info['attach_bt'])
        self.m_click(text=self.mesg_info['camera'])
        self.m_click(resourceId=self.mesg_info['takept'])
        logging.info('photo attach done')

    def send(self):
        """发送按钮"""
        self.m_click(resourceId=self.mesg_info['send_bt'])
        if self.m_ele_exists(resourceId=self.mesg_info['cost']):
            self.m_click(resourceId=self.mesg_info['sure'])
        logging.info('send done')

    def click_setting(self):
        """进入信息设置"""
        self.click_option()
        self.m_click(text=self.mesg_info['setting'])
        logging.info('click message settings')

    def mesg_exists(self):
        """判断是否有信息存在"""
        return self.m_ele_exists(resourceId=self.mesg_info['mesg_list'])

    def select_mesg(self):
        """选择要转发的信息"""
        self.m_click(resourceId=self.mesg_info['mesg_list'],
                     index=0)
        self.m_long_click(resourceId=self.mesg_info['session_list'])
        logging.info('one message select done')

    def click_option(self):
        """点击选项菜单，在信息内容列表界面"""
        self.m_click(description=self.mesg_info['option_list'])
        logging.info('click more option done')

    def forward_to_new(self):
        """"选择使用新信息转发
        点击选项菜单-选择转发-选择使用新信息"""
        self.m_click(resourceId=self.mesg_info['forward_bt'], index=1)
        self.m_click(resourceId=self.mesg_info['for_new'])
        logging.info('click forward message')

    def click_all_meun(self, s_meun, t_meun):
        self.click_setting()
        self.m_click(text=s_meun)
        if s_meun == 'Hear outgoing message sounds':
            logging.info('on/off bt')
        else:
            t = self.m_get_ele_text(text=t_meun)
            assert t in t_meun
