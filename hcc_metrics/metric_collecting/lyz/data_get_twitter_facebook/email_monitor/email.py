#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText  # 引入smtplib和MIMEText

def email(content):
    host = 'smtp.163.com'  # 设置发件服务器地址
    port = 25  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
    sender = 'liyaozongheu1@163.com'  # 设置发件邮箱
    # pwd=osseanrank0
    pwd = 'osseanrank0'  # 设置发件邮箱的密码，等会登陆会用到
    receiver = '2360539570@qq.com'  # 设置邮件接收人，填上自己的邮箱
    body = content  # 设置邮件正文，这里是支持HTML的

    msg = MIMEText(body, 'html')  # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = 'ossean_rank_error'  # 设置邮件标题
    msg['from'] = sender  # 设置发送人
    msg['to'] = receiver  # 设置接收人

    try:
        s = smtplib.SMTP(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(sender, pwd)  # 登陆邮箱
        s.sendmail(sender, receiver, msg.as_string())  # 发送邮件！
        print('Done')
    except smtplib.SMTPException:
        print("sb")
if __name__ == '__main__':
    email("ayo")

