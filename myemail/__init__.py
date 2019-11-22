from smtplib import SMTP#发送邮件包
from email.mime.text import MIMEText #发送字符串的邮件


def mySendMail():
    serveradr = 'c2.icoremail.net'
    sender = 'cqiang@dxdragon.cn'
    passwd = 'chen659758'
    receiver = ['cqiang@dxdragon.cn']
    subject = 'xx测试测试完成，请查看测试报告'
    contect = r'测试报告地址:\\192.168.1.139\report ' \
              r'需要将测试报告COPY至本地才能显示'

    msg = MIMEText(_text=contect)
    # ,_subtype='plain',_charset='utf-8')
    msg['From'] = sender  # 发件人
    msg['To'] = ";".join(receiver)  # 发件人,只能为字符串，多个收件人以分号隔开
    msg['Cc'] = ';'.join(receiver)  #抄送
    msg['Subject'] = subject  # 邮件主题

    # 发送邮件
    mail = SMTP(serveradr)  # 实例化SMTP服务器
    mail.set_debuglevel(1)
    mail.login(user=sender, password=passwd)  # 登录SMTP服务器
    mail.sendmail(sender, receiver, msg=msg.as_string())  # 发送邮件
    mail.quit()  # 退出


if __name__ == '__main__':
    mySendMail()