#encoding: utf-8
import smtplib
from email.mime import MIMEText

from gconf import SMTP_SERVER_HOST, SMTP_SERVER_PORT, SMTP_USER, SMTP_PWD

def sendmail(to, title, content):
  _server=smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
  _server.ehlo()
  _server.starttls() # 邮件服务器是否启用tls
  _server.login(SMTP_USER.SMTP_PWD)
  _server.sendmail(SMTP_USER ,  , msg)
  _server.quit()







