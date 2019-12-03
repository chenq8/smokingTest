import os
import time
import tkinter as tk
from threading import Thread
from tkinter import ttk
import ctypes
import inspect
import project_conf
import m_main
import logging


def __async_raise(thread_Id, exctype):
    """线程结束实现"""
    thread_Id = ctypes.c_long(thread_Id)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, None)
        raise SystemError("PyThreadState_SEtAsyncExc failed")


def terminator(thread):
    # 结束线程
    __async_raise(thread.ident, SystemExit)


class m_window():
    def __init__(self):
        self.root = None
        self.app_list = ['all', 'call', 'contact', 'message', 'chrome']
        self.count_list = [1, 5, 10, 15, 20, 25, 30, 50, 100]
        # 窗口的宽高
        self.window_width = None
        self.window_height = None
        # 各控件的textvariable
        self.test_log_val = None
        self.test_app_val = None
        self.test_count_val = None
        self.text_log_view = None
        self.read_file_thread = None

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
        app_list_box.current(4)
        test_app_lab.pack(side=tk.LEFT, )
        app_list_box.pack(side=tk.LEFT, padx=10)

        # 重复次数
        repeat_count = tk.Label(args_frame,
                                text='Test Repeat Count')
        repeat_count_box = ttk.Combobox(args_frame,
                                        text='test count',
                                        values=self.count_list,
                                        textvariable=self.test_count_val,
                                        )
        repeat_count_box.current(0)

        repeat_count.pack(side=tk.LEFT, padx=10)
        repeat_count_box.pack(side=tk.LEFT)
        return args_frame

    def view_log_frame(self):
        """log显示框架"""
        # 运行log显示文本框
        root = self.root
        log_frame = tk.Frame(root)

        test_log = tk.Label(log_frame, text='Test Log')
        self.text_log_view = tk.Text(log_frame,
                                     height=self.window_height / 17,
                                     )
        test_log.pack(anchor=tk.W)
        self.text_log_view.pack(fill='both', pady=10)
        return log_frame

    def run_frame(self):
        """运行停止按键框架"""
        root = self.root
        pad_val = self.window_width / 15
        bt_width = 9
        run_frame = tk.Frame(root, )
        # 执行和停止
        run_bt = tk.Button(run_frame,
                           text='run',
                           width=bt_width,
                           command=self.run_case,
                           # command=m_main.test_main
                           )

        stop_bt = tk.Button(run_frame,
                            text='stop',
                            width=bt_width,
                            command=self.stop_case)
        # 查看截图
        view_screenshot_bt = tk.Button(run_frame,
                                       text='View Screenshot',
                                       command=self.open_screenshot
                                       )
        # 查看报告
        view_report_bt = tk.Button(run_frame,
                                   text='View Report',
                                   command=self.open_report
                                   )

        view_report_bt.pack(side=tk.RIGHT, padx=10)
        view_screenshot_bt.pack(side=tk.RIGHT, padx=pad_val)
        stop_bt.pack(side=tk.RIGHT, padx=10)
        run_bt.pack(side=tk.RIGHT, padx=pad_val)
        return run_frame

    def run_case(self):
        """"启动测试"""
        app = self.test_app_val.get()
        count = self.test_count_val.get()
        m_main.main(app, count, )
        self.read_file_thread = Thread(target=self.read_log, )
        self.read_file_thread.setDaemon(True)
        self.read_file_thread.start()

    def stop_case(self):
        m_main.stop()
        self.text_log_view.insert('end', 'Test Process is stoped'+'\n')
        try:
            terminator(self.read_file_thread)
        except:
            logging.exception('thread error:')

    def open_report(self):
        """打开测试报告文件夹"""
        if os.path.exists(project_conf.REPORT_DIR):
            os.system('start explorer %s' % project_conf.REPORT_DIR)
        else:
            logging.info('can not open this report dir,check exists?')

    def open_screenshot(self):
        """打开失败截图文件夹"""
        if os.path.exists(project_conf.SCREENSHOT_DIR):
            os.system('start explorer %s' % project_conf.SCREENSHOT_DIR)
        else:
            logging.info('can not open this screenshot dir,check exists?')

    def read_log(slef):
        position = 0
        with open(project_conf.LOG_PATH, mode='r', encoding='utf8') as f1:
            while True:
                line = f1.readline().strip()
                if line:
                    slef.text_log_view.insert('end', line + '\n')
                    slef.text_log_view.see('end')
                cur_position = f1.tell()  # 记录上次读取文件的位置
                if cur_position == position:
                    time.sleep(0.1)
                    continue
                else:
                    position = cur_position

    def main_window(self):
        """窗口主入口"""

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
        root.mainloop()


if __name__ == '__main__':
    m_window().main_window()
