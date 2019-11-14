import yaml
import os
class MyData:
    """读取配置文件"""

    def __init__(self):
        self.appdata = None

    def load_data(self,configpath):
        """加载配置文件"""
        print(configpath)
        with open(configpath, 'r',
                  encoding='utf-8') as file:
            files = file.read()
        return yaml.load(files, Loader=yaml.SafeLoader)

    # def load_app_date(self,path):
    #     """加载配置信息"""
    #     app_path = r'D:\mytools\SmokingTestCase\testdata\contact.yaml'
    #     self.appdata = self.loadfile(app_path)
    #     return self.appdata


if __name__=='__main__':
    data = MyData()
    # data.load_app_date()
    # print(os.getcwd())
    path=os.path.join(os.path.split(os.getcwd())[0],'testdata','contact.yaml')
    s = data.load_data(path)
    print(s['secondary_meun'])
