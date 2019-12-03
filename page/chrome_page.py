from page.base import Base
import logging
import project_conf


class Chrome(Base):
    def __init__(self):
        self.chrome_info = self.m_get_data('chrome.yaml')

    def start_chrome(self):
        """打开应用，暂时无法通过app_start打开"""
        self.m_click_home()
        self.m_click(text='Chrome')

    def skip_welcome(self):
        """跳过欢迎界面，点击允许和跳过登录"""
        if self.m_ele_exists(resourceId=self.chrome_info['accept']):
            self.m_click(resourceId=self.chrome_info['accept'])
            self.m_click(resourceId=self.chrome_info['no_login'])
            logging.info('skip welcome done')

    def input_url(self,url):
        """打开百度
        如果有欢迎页，刚跳过，点击地址栏，输入网址"""
        self.skip_welcome()
        if self.m_ele_exists(resourceId=self.chrome_info['input_url']):
            self.m_click(resourceId=self.chrome_info['input_url'])
            self.m_input(url, resourceId=self.chrome_info['top_url'])
        else:
            self.m_input(url, resourceId=self.chrome_info['top_url'])
        self.m_input_enter()
        logging.info('search done')

    def get_baidu_text(self):
        """返回百度搜索按钮的文本
        如果有位置权限提示，则关闭后取值"""
        if self.m_ele_exists(resourceId=self.chrome_info['location']):
            self.m_click(resouredId=self.chrome_info['location'])

            return self.m_get_ele_text(resourceId=self.chrome_info['search_bt'])

        else:
            return self.m_get_ele_text(resourceId=self.chrome_info['search_bt'])


    def click_meun(self):
        self.m_click(resourceId=self.chrome_info['meun'])
        logging.info('click chrome main meun done')

    def click_setting(self):
        self.m_click(text=self.chrome_info['setting'])
        logging.info('click chrome settings')
        self.m_scroll_to_end()
