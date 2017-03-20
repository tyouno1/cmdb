#encoding: utf-8
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

from gconf import SMTP_SERVER_HOST, SMTP_SERVER_PORT, SMTP_USER, SMTP_PWD

def sendmail(to_list, title, content):
  _server=smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
  _server.set_debuglevel(True)
  _server.ehlo()
  #_server.starttls() # 邮件服务器是否启用tls
  _server.login(SMTP_USER, SMTP_PWD)
  _msg = MIMEText(content,'html','utf-8')
  _msg['Subject'] = title
  _msg['To'] = ';'.join(to_list)
  _msg['From'] = '51reboot告警管理员<%s>' % SMTP_USER
  _msg['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  _server.sendmail(SMTP_USER , to_list , _msg.as_string())
  _server.quit()

if __name__ == '__main__':
  sendmail(['zhangqino2@126.com'],'告警邮件','cpu内存告警测试')

