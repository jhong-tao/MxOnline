#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
==================================================
@Project -> File   ：MxOnline -> YunPian.py
@IDE    ：PyCharm
@Author ：jhong.tao
@Date   ：2021/6/7 10:34
@Desc   ：发送手机短信验证码
==================================================
"""
import requests  # requests是python提供的url请求的工具包
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import json


def send_single_sms(apikey, code, mobile):
    """
    云片网接口实现短信验证码，发送
    云片网API:https://www.yunpian.com/official/document/sms/zh_cn/domestic_single_send
    send_single_sms：方法用来通过云片网发送单条短信
    :param apikey: 云片网的apikey
    :param text: 发送的短信内容，比如验证码
    :param mobile: 目的手机号码
    :return: 返回json类型的验证码发送详情信息
    """
    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    text = '【蜗犇AI】您的验证码是{}'.format(code)  # 发送的短信内容，text模板需要自己去云片网申请
    res = requests.post(url, data={
        'apikey': apikey,
        'mobile': mobile,
        'text': text
    })
    res_json = json.loads(res)
    return  res_json


# sender_qq为发件人的qq号码
sender_qq = 'jhong.tao'
# pwd为qq邮箱的授权码
pwd = 'fnhcfchhjqticibj'
# 收件人邮箱receiver
receiver = 'thunder***@gmail.com'
# 邮件的正文内容
mail_content = '你好，你的验证码为{}'.format('随机数')
# 邮件标题
mail_title = '【蜗犇AI】验证码'


def send_mail(sender_qq='', pwd='', receiver='', mail_title='', mail_content=''):
    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    sender_qq_mail = sender_qq + '@qq.com'

    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()

