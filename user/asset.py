#encoding: utf-8
from mutils import execute_fetch_sql , execute_commit_sql

'''
create table assets (
  id int primary key auto_increment,
  sn varchar(128) not null default '' unique key comment 'sn编码',
  ip varchar(128) default '' not null comment 'ip地址',
  hostname varchar(64) not null default '' comment '主机名',
  os varchar(32) not null default '' comment  '操作系统',
  cpu int not null default 0 comment 'cpu核数',
  ram int not null default 0 comment '内存(G)',
  disk int not null comment '磁盘大小(G)',
  idc_id int not null comment '机房ID',
  admin varchar(32) not null default '使用者',
  business varchar(32) default '' comment '业务',
  purchase_date datetime not null comment '采购日期',
  warranty int not null comment '报修时间(年)',
  vendor varchar(64) default '' comment '供应商',
  model varchar(64) default '' comment '型号',
  status int not null default 0
) engine=INNODB default charset=utf8;
'''

def get_idc_list():
  _sql = 'SELECT id , name  FROM idcs where status = 0'
  _cnt, _rt_list = execute_fetch_sql(_sql)
  return _rt_list

'''
返回所有资产信息
[
  {"sn":"" , "id":"", "hostname":"", "ip":"", ...},
  {},
  {}
]
'''
def get_list():
  _column = 'id, sn, ip, hostname, os, cpu, ram, disk,idc_id,admin,business,purchase_date,warranty, vendor, model'
  _sql = 'SELECT {columns} FROM assets where status = 0'.format(columns=_column)
  _cnt, _rt_list = execute_fetch_sql(_sql)
  return _cnt, _rt_list

'''
通过主键返回资产信息
None/{}
'''
def get_by_id(aid):
  _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
  _sql = 'SELECT {columns} FROM assets where status=0 and id=%s'.format(columns=_column)
  _args = (aid,)
  _cnt, _rt_list = execute_fetch_sql(_sql, _args)
  return _cnt, _rt_list

'''
通过sn返回资产信息
None/{}
'''
def get_by_sn(sn):
  _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
  _sql = 'SELECT {columns} FROM assets where status=0 and sn=%s'.format(columns=_column)
  _args = (sn,)
  execute_fetch_sql(_sql, _args)
  _cnt, _rt_list = execute_fetch_sql(_sql)
  return _rt_list


'''
在创建资产时对输入信息进行检查
True/False, error_msg{}
'''
def validate_create(asset):
  _is_ok = True
  _errors = {}

  '''
  字符串类型：sn, ip, hostname, os, admin, business, vendor, model
  检查是否为空(不允许),最小长度，最大长度
  '''
  for _key in 'sn,ip,hostname,os,admin,business,vendor,model'.split(','):
    _value = asset.get(_key,'').strip()
    if _value == '':
      _is_ok = False
      _errors[_key] = '%s不允许为空' % _key
    elif len(_value) > 64:
      _is_ok = False
      _errors[_key] = '%s不允许超过64个字符' % _key

  if get_by_sn(asset.get('sn')):
    _is_ok = False
    _errors[_key] = 'sn已经存在'

  '''
  取值类型:idc_id
  '''
  _idc_id =  asset.get('idc_id')
  if int(_idc_id) not in [ _idc['id'] for _idc in get_idc_list()]:
    _is_ok = False
    _errors['idc'] = '机房选择不正确'

  '''
  数字类型：cpu, ram, disk, warranty
  检查数字类型isdigit, 最大值，最小值
  '''
  _rules = {
    'cpu': {'min': 2, 'max': 64},
    'ram': {'min': 2, 'max': 512},
    'disk': {'min': 2, 'max': 2048},
    'warranty': {'min': 1, 'max': 5},
  }

  for _key in 'cpu,ram,disk,warranty'.split(','):
    _value = asset.get(_key, '').strip()
    print _key, _value
    if not _value.isdigit():
      _is_ok = False
      _errors[_key] = '%s不是整数' % _key
    else:
      _value = int(_value)
      _min = _rules.get(_key).get('min')
      _max = _rules.get(_key).get('max')
      if _value < _min or _value > _max:
        _is_ok = False
        _errors[_key] = '%s取值范围应该为%s ~ %s' % (_key, _min, _max)

    '''
    日期类型：purchase_date
    '''
    if not asset.get('purchase_date',''):
      _is_ok = False
      _errors['purchase_date'] = '采购日期不能为空'

  return _is_ok, _errors

'''
在创建资产时输入信息进行检查
True/False, error_msg{}
'''
def create(asset):
  _column_str = 'sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
  _columns = _column_str.split(',')
  _args = []
  for _column in _columns:
    _args.append(asset.get(_column,''))
  _sql = 'INSERT INTO assets({columns}) values({values})'.format(columns=_column_str,values=','.join(['%s'] * len(_columns)))
  _cnt, _rt_list = execute_commit_sql(_sql, _args)
  return _cnt, _rt_list

'''
在修改资产时对输入信息进行检查
True/False, error_msg{}
'''
def validate_update(asset):
  return True, {}

'''
更新资产，操作数据库
返回True/False
'''
def update(asset):
  _column_str = 'ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
  _columns = _column_str.split(',')
  _values = []
  _args = []
  for _column in _columns:
    _values.append('{column}=%s'.format(column=_column))
    _args.append(asset.get(_column,''))
  _args.append(asset.get('id'))

  _sql ='UPDATE assets SET {values} WHERE id=%s'.format(values=','.join(_values))
  _cnt, _rt_list = execute_commit_sql(_sql, _args)
  return _cnt, _rt_list

'''
删除资产，操作数据库
返回True/False
'''
def delete(aid):
  _sql = 'UPDATE assets set status=1 where id =%s'
  _args = (aid,)
  _cnt, _rt_list = execute_commit_sql(_sql, _args)
  return _cnt, _rt_list

if __name__ == '__main__':
  print get_list()
