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

report_path="/tmp/rc_functional_test/room_control/report/"

def main():
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
        #print 1
        sys.exit(1)
    else:
        #print 0 
        sys.exit(0)

if __name__=='__main__':
    main()
