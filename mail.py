#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
    This script use to send email. and modify from
    http://www.juyimeng.com/
    simple-python-send-mail-sample-code-with-smtp-auth.html
"""

import smtplib
from email.mime.text import MIMEText

#To somebody
mail_to_list=["work_complete@163.com"]
#the mail server
mail_host="smtp.xmu.edu.cn"
#most mail server need login with password
mail_user="20520101151597@stu.xmu.edu.cn"
mail_pass="eaglewong"

mail_postfix="stu.xmu.edu.cn"


def send_mail(to_list,sub,content):
    """
        send_mail       send email
            to_list
            sub         subject
            content     the content of email
    """
    
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    print( msg['To'] )
    try:
        s = smtplib.SMTP(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print( str(e) )
        return False
if __name__ == '__main__':
    if send_mail(mail_to_list,"subject","content"):
        print "sent sucessful"
    else:
        print "Failed to send mail"
