#encoding:utf-8
import gconf
import json
import MySQLdb
from dbutils import execute_fetch_sql , execute_commit_sql

''' 数据库结构
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(32) NOT NULL,
  `age` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into user (username , password, age) values ('kk',md5('123456'),20);
'''

''' 获取所有用户的信息
返回值: [
          {"username":"kk", "password":"123456, "age":29},
          {"username":"woniu", "password":"123", "age":28}
        ]   
'''
def get_users(wheres=[]):
  _columns = ('id','username','password','age')
  _sql = "select * from user where 1=1"
  _args = []
  for _key , _value in wheres:
    _sql += ' AND {key} = %s'.format(key=_key)
    _args.append(_value)

  _count, _rt_list = execute_fetch_sql(_sql,_args)
  _rt = []
  for _line in _rt_list:
    _rt.append(dict(zip(_columns,_line)))
  return _rt

# 保存用户数据到文件
def save_users(users):
  fhandler = open(gconf.USER_FILE, 'wb')
  fhandler.write(json.dumps(users))
  fhandler.close()

# 验证用户名，面膜是否正确
def validate_login(username, password):
  #_sql = "select * from user where username='{username}' and password=md5('{password}')".format(username=username, password=password)
  _sql = "select * from user where username=%s and password=md5(%s)"
  _count, rt_list = execute_fetch_sql(_sql, (username, password))
  return _count !=0 
  #if _count == 0:
  #  return False
  #else:
  #  return True
  
def validate_add_user(username , password, age):
  if username.strip() == '':
    return False,u'用户名不能为空'

  #检查用户名是否重复
  _user = get_user(username)
  if _user and _user.get('username') == username:
    return False, u'用户名已存在'

  #密码要求长度必须大于等于6
  if len(password) < 6:
    return False, u'密码长度必须大于等于6'

  if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
    return False, u'年龄必须是0到100的数字'

  return True, ''

#添加用户信息
def add_user(username, password, age):
  _sql = 'insert into user (username, password, age) values (%s,md5(%s),%s)'
  _args = (username, password, age)
  execute_commit_sql(_sql, _args)

#获取用户信息
def get_user(username):
  _rt = get_users([('username',username)])
  print _rt
  return _rt[0] if len(_rt) else None

#检查更新用户信息
def validate_udpate_user(username, password, age):
  if get_user(username) is None:
    return False, u'用户信息不存在'

#  #密码要求长度必须大于等于6
#  if len(password) < 6:
#    return False, u'密码长度必须大于等于6'

  if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
    return False, u'年龄必须是0到100的数字'

  return True, ''
  
#更新用户信息
def update_user(username, password, age):
  _sql = 'update user set age=%s where username=%s'
  execute_commit_sql(_sql,(age,username))

#删除用户信息
def delete_user(username):
  _sql = 'delete from user where username=%s'
  execute_commit_sql(_sql,(username,))

def validate_change_user_password(username, upassword, musername, mpassword):
  # 检查管理员密码是否争取
  if not validate_login(musername, mpassword):
    return False, u'管理员密码错误'

  if get_user(username) is None:
    return False, u'用户信息不存在'

  if len(upassword) < 6:
    return False, u'密码长度必须大于等于6'

  return True, ''

def change_user_password(username, upassword):
  _sql = 'update user set password=md5(%s) where username =%s'
  execute_commit_sql(_sql,(upassword,username))

if __name__ == '__main__':
  pass
