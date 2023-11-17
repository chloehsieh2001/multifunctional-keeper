#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:51:51 2020

@author: larry
"""
import os
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

datetime_dt = datetime.datetime.today()
datetime_str = datetime_dt.strftime("%Y-%m-%d") 

basepath = os.path.join(os.path.dirname(__file__), 'static','send')
gmail_user = 'qf.finalproject@gmail.com'
gmail_password = 'qf108071036'
from_address = gmail_user
dirs = os.listdir(basepath) 
if '.DS_Store' in dirs:
    dirs.remove('.DS_Store')
for i in range(0,len(dirs)):
    if datetime_str in dirs[i]:
           
        with open(basepath + '/' + dirs[i],'r') as m:
            ml = [line.rstrip('\n') for line in m]
        
        mail = MIMEMultipart()
        mail['From'] = from_address
        mail['To'] = ' ,'.join([ml[0]])
        mail['Subject'] = ml[1]
        mail.attach(MIMEText(ml[2]))
    
        smtpserver = smtplib.SMTP_SSL('smtp.gmail.com',465)
        smtpserver.ehlo()
        
        smtpserver.login(gmail_user,gmail_password)
    
        smtpserver.sendmail(from_address,ml[0],mail.as_string())
        smtpserver.quit()
