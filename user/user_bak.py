#encoding:utf-8
import gconf
import json

''' 获取所有用户的信息
返回值: [
          {"username":"kk", "password":"123456, "age":29},
          {"username":"woniu", "password":"123", "age":28}
        ]   
'''
def get_users():
  try:
    handler = open(gconf.USER_FILE, 'rb')
    cxt = handler.read()
    handler.close()
    return json.loads(cxt)
  except:
    return []

# 保存用户数据到文件
def save_users(users):
  fhandler = open(gconf.USER_FILE, 'wb')
  fhandler.write(json.dumps(users))
  fhandler.close()

# 验证用户名，面膜是否正确
def validate_login(username, password):
  users = get_users()
  for user in users:
    if user.get('username') == username and user.get('password') == password:
      return True
  return False

# 检查新建用户信息
def validate_add_user(username , password, age):
  if username.strip() == '':
    return False,u'用户名不能为空'

  #检查用户名是否重复
  _users = get_users()
  for _user in _users:
    if username == _user.get('username'):
      return False, u'用户名已存在'

  #密码要求长度必须大于等于6
  if len(password) < 6:
    return False, u'密码长度必须大于等于6'

  if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
    return False, u'年龄必须是0到100的数字'

  return True, ''

#添加用户信息
def add_user(username, password, age):
  _user = {'username':username, 'password':password, 'age':age}
  _users = get_users()
  _users.append(_user)
  save_users(_users)

#获取用户信息
def get_user(username):
  _users = get_users()
  for _user in _users:
    if _user.get('username') == username:
      return _user
  return None

#检查更新用户信息
def validate_udpate_user(username, password, age):
  if get_user(username) is None:
    return False, u'用户信息不存在'

  #密码长度必须大于等于6
  if len(password) < 6:
    return False, u'密码必须大于等于6'

  #密码要求长度必须大于等于6
  if len(password) < 6:
    return False, u'密码长度必须大于等于6'

  if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
    return False, u'年龄必须是0到100的数字'

  return True, ''
  
#更新用户信息
def update_user(username, password, age):
  _users = get_users()
  for _user in _users:
    if _user.get('username') == username:
      _user['password'] = password
      _user['age'] = age
      save_users(_users)
      break

#删除用户信息
def delete_user(username):
  _users = get_users()
  _idx = -1
  for _user in _users:
    _idx += 1
    if _user.get('username') == username:
      del _users[_idx]
      save_users(_users)
      break

if __name__ == '__main__':
  pass
