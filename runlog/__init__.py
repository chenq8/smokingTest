import smtplib
# from email.mime.application import MIMEApplication
# from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mySendMail():
    serveradr = 'c2.icoremail.net'
    sender = 'cqiang@dxdragon.cn'
    passwd = 'chen659758'
    receiver = ['cqiang@dxdragon.cn']
    subject = '测试邮件主题'
    contect = r'‪测试报告地址：\\192.168.1.139\report\index.html'

    # 标准邮件需要三个头部信息： From, To, 和 Subject
    """_text为邮件发送的内容
        _subtype为邮件内容的格式，使用默认plain的就好，
        发送HTML格式文件时将其设置为html
        _charset文字编码,默认为空,会自动判断编码格式，源码如下：
        if _charset is None:
                try:
                    _text.encode('us-ascii')
                    _charset = 'us-ascii'
                except UnicodeEncodeError:
                    _charset = 'utf-8'
                    """
    msg = MIMEText(_text=contect)
    # ,_subtype='plain',_charset='utf-8')
    msg['From'] = sender  # 发件人
    msg['To'] = ";".join(receiver)  # 发件人,只能为字符串，多个收件人以分号隔开
    msg['Cc'] = ';'.join(receiver)  #抄送
    msg['Subject'] = subject  # 邮件主题

    # 发送邮件
    mail = smtplib.SMTP(serveradr)  # 实例化SMTP服务器
    mail.set_debuglevel(1)
    mail.login(user=sender, password=passwd)  # 登录SMTP服务器
    mail.sendmail(sender, receiver, msg=msg.as_string())  # 发送邮件
    mail.quit()  # 退出

# def addAnnex():
#     """
#     流程
#     1.设置附件路径
#     2.使用MIMEApplication读取文件内容
#     3.使用add_header添加在邮件中显示的内容
#     4.实例化MIMEMultipart对象，添加附件进邮件"""
#     filedir = 'e:log.log'
#     testAnnex = MIMEApplication(open(filedir,'rb').read())
#     testAnnex.add_header('Content-Disposition', 'attachment',filename = 'mmmmmm.txt')
#     return testAnnex
#     annex.attach(MIMEText('带有附件的邮件'))#邮件正文
#     annex  = MIMEMultipart()
#     annex.attch(addAnnex())

if __name__=="__main__":
    mySendMail()