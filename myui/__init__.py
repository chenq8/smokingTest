import tkinter as tk
from tkinter import ttk
import m_main


class m_window():
    def __init__(self):
        self.root = None
        self.app_list = ['all','call', 'contact', 'message', 'chrome']
        self.count_list = [1,5,10,15,20,25,30,50,100]
        self.window_width = None
        self.window_height = None
        self.test_log_text = None
        self.test_app_val = None
        self.test_count_val = None

    def set_screen_senter(self):
        # 设置窗口屏幕居中显示
        root = self.root
        sw = root.winfo_screenwidth()  # 宽
        sh = root.winfo_screenheight()  # 高
        self.window_width = sw / 2.5
        self.window_height = sh / 1.5
        x = (sw - self.window_width) / 20
        y = (sh - self.window_height) / 20
        root.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, x, y))

    def args_frame(self):
        root = self.root
        args_frame = tk.Frame(root)
        self.test_app_val = tk.StringVar()
        self.test_count_val = tk.IntVar()

        # 测试app下拉列表
        test_app_lab = tk.Label(args_frame,
                                text='Test App')
        app_list_box = ttk.Combobox(args_frame,
                                    text='app list',
                                    values=self.app_list,
                                    state='readonly',
                                    textvariable=self.test_app_val
                                    )
        app_list_box.current(0)
        test_app_lab.pack(side=tk.LEFT, )
        app_list_box.pack(side=tk.LEFT, padx=10)
        # 创建事件，当下拉选择一个值时，执行set_test_app方法
        app_list_box.bind("<<ComboboxSelected>>", self.set_test_app)


        # 重复次数
        repeat_count = tk.Label(args_frame,
                                text='Test Repeat Count')
        repeat_count_box = ttk.Combobox(args_frame,
                                        text='test count',
                                        values=self.count_list,
                                        textvariable=self.test_count_val,
                                        )
        repeat_count_box.bind("<<ComboboxSelected>>", self.set_test_count)

        repeat_count.pack(side=tk.LEFT, padx=10)
        repeat_count_box.pack(side=tk.LEFT)
        return args_frame

    def view_log_frame(self):
        # 运行log显示文本框
        root = self.root
        log_frame = tk.Frame(root)
        test_log = tk.Label(log_frame, text='Test Log')
        self.test_log_text = tk.Text(log_frame,
                                     textvariable=None,
                                     height=self.window_height / 17,
                                     )
        test_log.pack(anchor=tk.W)
        self.test_log_text.pack(fill='both', pady=10)
        return log_frame

    def run_frame(self):
        root = self.root
        pad_val = self.window_width / 15
        bt_width = 9
        run_frame = tk.Frame(root, )
        # 执行和停止
        run_bt = tk.Button(run_frame,
                           text='run',
                           width=bt_width,
                           command=m_main.main,
                           # command=m_main.main
                           )

        stop_bt = tk.Button(run_frame,
                            text='stop',
                            width=bt_width,
                            command=self.set_test_app)
        # 查看截图
        view_screenshot_bt = tk.Button(run_frame,
                                       text='View Screenshot',
                                       )
        # 查看报告
        view_report_bt = tk.Button(run_frame,
                                   text='View Report',
                                   )

        view_report_bt.pack(side=tk.RIGHT, padx=10)
        view_screenshot_bt.pack(side=tk.RIGHT, padx=pad_val)
        stop_bt.pack(side=tk.RIGHT, padx=10)
        run_bt.pack(side=tk.RIGHT, padx=pad_val)
        return run_frame

    def main_window(self):
        self.root = tk.Tk()
        root = self.root
        # root = tk.Tk()
        root.title('YuaYi Auto Test Platform')
        self.set_screen_senter()
        root.resizable(0, 0)  # 窗口不可调在大小

        self.args_frame().pack(fill='x',
                               padx=10, pady=10,
                               )
        self.view_log_frame().pack(fill='x',
                                   padx=10, pady=10,
                                   )
        self.run_frame().pack(fill='x', )
        root.mainloop()  # 进入消息循环（必需组件）

    def set_test_app(self,event):
        """设置测试的APP"""
        # project_conf.TEST_APP = self.test_app_val.get()
        # print(project_conf.TEST_APP)
        return self.test_app_val.get()

    def set_test_count(self,event):
        # project_conf.TEST_COUNT = self.test_count_val.get()
        # print(project_conf.TEST_COUNT)
        return self.test_count_val.get()


if __name__ == '__main__':
    m_window().main_window()
