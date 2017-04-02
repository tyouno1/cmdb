#encoding: utf-8
import time
CNT = 3
CPU_PERCENT = 7
RAM_PERCENT = 8
from dbutils_class import MySQLConnection
from mailutil import sendemail
from gconf import ALARM_RECIVERS
import logging
import datetime
import asset

logger = logging.getLogger(__name__)

def has_alarm(ip):
  _sql = 'select cpu, ram from performs where ip = %s and time > %s order by time desc limit %s'
  _time = datetime.datetime.now() - datetime.timedelta(minutes=5)
  _args = (ip, _time.strftime('%Y-%m-%d %H:%M:%S') , CNT)
  _rt_cnt, _rt_list = MySQLConnection.execute_sql(_sql,_args)
  
  print _rt_cnt , _rt_list

  if _rt_cnt < CNT:
    return False, False
  
  _cpu_alarm = True
  _ram_alarm = True
  for _cpu, _ram in _rt_list:
    if _cpu < CPU_PERCENT:
      _cpu_alarm = False

    if _ram < RAM_PERCENT:
      _ram_alarm = False
    
  return _cpu_alarm, _ram_alarm
    

def monitor():
  #_ip_list = ['192.168.137.101']
  _cnt, _asset_list = asset.get_list()
  _title = 'CPU&内存告警'
  for _asset in _asset_list:
    _ip = _asset['ip']
    _cpu_alarm, _ram_alarm =  has_alarm(_ip)
    _content_list = ['主机{ip}告警'.format(ip=_ip)]
    if _cpu_alarm:
      _content_list.append('CPU连续 {cnt} 次超过{percent}%'.format(cnt=CNT, percent=CPU_PERCENT))
    if _ram_alarm:
      _content_list.append('内存连续 {cnt} 次超过{percent}%'.format(cnt=CNT, percent=RAM_PERCENT))

    # 有报警内容才发送邮件
    if len(_content_list) >= 2:
      # 发送邮件
      sendemail(ALARM_RECIVERS,_title,','.join(_content_list))
      logger.info('send mail to:%s, titile: %s,  msg:%s', ALARM_RECIVERS, _title, ','.join(_content_list))

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)s [%(lineno)d] %(levelname)s %(message)s',
    filename="monitor.log")
  monitor()
