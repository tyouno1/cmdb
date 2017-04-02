#!/usr/bin/env python
#encoding: utf-8

import logging
import time
import os
import requests
import json
import traceback

APP_KEY = '90cf05e93e7e824b93eb12a22f5cbbae'
APP_SECRET = '94e839465545c03bcb0078e6af42cd5e'

#SERVER_URL = 'http://192.168.137.101:9001/performs/?app_key={app_key}&app_secret={app_secret}'.format(app_key=APP_KEY,app_secret=APP_SECRET)
SERVER_URL = 'http://192.168.137.101:9001/performs/'

logger = logging.getLogger(__name__)

def execute_cmd(cmd):
  _fh = os.popen(cmd)
  _cxt = _fh.read()
  _fh.close()
  return _cxt

def get_ip():
  _cmd = "ifconfig eth0 | grep 'inet addr' | awk '{print $2}'"
  _cxt = execute_cmd(_cmd)
  return str(_cxt.split(':')[-1]).strip()

def collect_cpu():
  _cmd = "top -n 1 | grep Cpu | awk '{print $5}'"
  _cxt = execute_cmd(_cmd)
  return 100 - float(_cxt.split('%')[0])

def collect_ram():
  _cmd = "top -n 1 | grep Cpu | awk '{print $5}'"
  _cxt = execute_cmd(_cmd)
  return 100 - float(_cxt.split('%')[0])

def collect_ram():
  _fh = open('/proc/meminfo')
  _total = float(_fh.readline().split()[1])
  _free = float(_fh.readline().split()[1])
  _buffer = float(_fh.readline().split()[1])
  _fh.close()
  return 100 - (_free + _buffer)*100 /_total

def collect():
  _rt = {}
  _rt['ip'] = get_ip()
  _rt['cpu'] = collect_cpu()
  _rt['ram'] = collect_ram()
  _rt['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
  return _rt

def send(msg):
  try:
    _reponse = requests.post(SERVER_URL, data=json.dumps(msg), headers={"Content-Type":"application/json","app_key":APP_KEY, 'app_secret':APP_SECRET})
    if not _reponse.ok:
      logger.error('error send msg %s', _msg)
    else:
      _json = _reponse.json()
      if _json.get('code') != 200:
        logger.error('error send msg %s , result:%s', _msg, _json)
  except BaseException as e:
    logger.error(traceback.format_exc())

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)s [%(lineno)d] %(levelname)s %(message)s',
    filename="agent.log")
  
  while True:
    try:
      _msg = collect()
      logger.debug(_msg)
      send(_msg)
      time.sleep(10)
    except BaseException as e:
      logger.error(traceback.format_exc())
