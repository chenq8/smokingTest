from page.base import Base


class Chrome(Base):
    def __init__(self):
        self.chrome_info = self.get_data('chrome.yaml')

    def start_chrome(self):
        """打开应用，暂时无法通过app_start打开"""
        self.mclick_home()
        self.mclick(text='Chrome')

    def skip_welcome(self):
        """跳过欢迎界面，点击允许和跳过登录"""
        if self.ele_exists(resourceId=self.chrome_info['accept']):
            self.mclick(resourceId=self.chrome_info['accept'])
            self.mclick(resourceId=self.chrome_info['no_login'])

    def input_url(self,url):
        """打开百度
        如果有欢迎页，刚跳过，点击地址栏，输入网址"""
        self.skip_welcome()
        if self.ele_exists(resourceId=self.chrome_info['input_url']):
            self.mclick(resourceId=self.chrome_info['input_url'])
            self.minput(url,resourceId=self.chrome_info['top_url'])
        else:
            self.minput(url,resourceId=self.chrome_info['top_url'])
        self.input_enter()

    def get_baidu_text(self):
        """返回百度搜索按钮的文本
        如果有位置权限提示，则关闭后取值"""
        if self.ele_exists(resourceId=self.chrome_info['location']):
            self.mclick(resouredId=self.chrome_info['location'])

            return self.get_ele_text(resourceId=self.chrome_info['search_bt'])

        else:
            return self.get_ele_text(resourceId=self.chrome_info['search_bt'])

    def click_meun(self):
        self.mclick(resourceId=self.chrome_info['meun'])

    def click_setting(self):
        self.mclick(text=self.chrome_info['setting'])
        self.scroll_to_end()