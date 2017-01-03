#!/usr/bin/env python
# -*- coding: utf-8 -*-

' email module '

__author__ = 'fengying.que'

import sys
import email  
import mimetypes  
from email.MIMEMultipart import MIMEMultipart  
from email.MIMEText import MIMEText  
from email.MIMEImage import MIMEImage  
import smtplib
from xml.etree import ElementTree as ET
reload(sys)
sys.setdefaultencoding('utf-8')

report_path="/tmp/rc_functional_test/room_control/report/"

def jixixml():
    tree = ET.parse(report_path + "output.xml")
    root = tree.getroot()
    flag = 0
    errorlist=[]
    for tc in root.findall('.//test'):
        name=tc.get("name")
        #print name
        for tc1 in tc.findall('.//status'):
            #print tc1
            zt=tc1.get("status")
            #print zt
            if zt=="FAIL":
                flag=flag+1
                errorlist.append(name)
                errorlist.append('\n')
                break
    if flag != 0:
        errorlist.append("上述接口调用失败")
    return errorlist


def sendHtml(authInfo, fromAdd, toAdd, subject, htmlText):  
    #设定HTML信息  
    msgText = MIMEText(htmlText, 'html', 'utf-8')  
    send(authInfo, fromAdd, toAdd, subject, msgText)


def sendPlainText(authInfo, fromAdd, toAdd, subject, plainText):
    #设定纯文本信息  
    msgText = MIMEText(plainText, 'plain', 'utf-8')
    send(authInfo, fromAdd, toAdd, subject, msgText)

def getMailSrv(authInfo):
    server = authInfo.get('server')  
    user = authInfo.get('user')  
    passwd = authInfo.get('password')  

    if not (server or user or passwd):
        smtp = smtplib.SMTP('localhost')
    else:
        smtp = smtplib.SMTP()  
       #设定调试级别，依情况而定  
        smtp.set_debuglevel(1)  
        smtp.connect(server)  
        smtp.login(user, passwd)
    return smtp



def send(authInfo, fromAdd, toAdd, subject, msgText):
    strFrom = fromAdd  
    strTo = ','.join(toAdd)

    # 设定root信息  
    msgRoot = MIMEMultipart('related')  
    msgRoot['Subject'] = subject  
    msgRoot['From'] = strFrom  
    msgRoot['To'] = strTo  
    msgRoot.preamble = 'This is a multi-part message in MIME format.'  
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    att1 = MIMEText(open( report_path + 'log.html','rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="log.html"'
    msgAlternative.attach(att1)
  

    #设定文本信息  
    msgAlternative.attach(msgText)
    
 
    smtp = getMailSrv(authInfo)
    smtp.sendmail(strFrom, strTo.split(','), msgRoot.as_string())
    smtp.quit()  
    return

def sendMail():
    authInfo = {}
    fromAdd = 'fengying.que@qunar.com'
    toAdd = ['fengying.que@qunar.com,wenzhong.feng@qunar.com']
    subject = 'SRM 功能测试结果'
    list=jixixml()
    listlen=len(list)
    if listlen == 0:
        plainText="ALL CASE PASSED"
    else:
        plainText = "" + ''.join(list) + ""
    htmlText = open( report_path + "log.html","r").read()
    # sendHtml(authInfo, fromAdd, toAdd, subject, htmlText)
    sendPlainText(authInfo, fromAdd, toAdd, subject, plainText)




