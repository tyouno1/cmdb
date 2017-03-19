#encoding:utf-8
from dbutils_class import MySQLConnection
#from dbutils import execute_fetch_sql , execute_commit_sql

class User(object):
  def __init__(self, username, password, age):
    self.username = username
    self.password = password
    self.age = age

  # 验证用户名，密码是否正确
  @classmethod
  def validate_login(cls, username, password):
    _column='username'
    _columns = _column.split(',')
    _sql = "select {column} from user where username=%s and password=md5(%s)".format(column=_column)
    _count, _rt_list = MySQLConnection.execute_sql(_sql, (username, password))
    return dict(zip(_columns , _rt_list[0])) if _count != 0 else None


  ''' 获取所有用户的信息
  返回值: [
          {"username":"kk", "password":"123456, "age":29},
          {"username":"woniu", "password":"123", "age":28}
        ]
  '''
  @classmethod
  def get_list(cls, wheres=[]):
    _column = 'username,password,age'
    _columns = _column.split(',')
    _sql = "select {column} from user where 1=1".format(column=_column)
    _args = []
    for _key , _value in wheres:
      _sql += ' AND {key} = %s'.format(key=_key)
      _args.append(_value)

    print _sql
    _count, _rt_list = MySQLConnection.execute_sql(_sql,_args)
    #返回一个User对象
    #_rt = []
    #for _line in _rt_list:
    #  _user_dict = dict(zip(_columns, _line))
    #  _user = User(_user_dict['id'], _user_dict['username'],_user_dict['password'],_user_dict['age'])
    #  _rt.append(_user)
    #return _rt

    # 简单的写法
    # User(**dict) = 将每个字典中的value传入
    return [User(**dict(zip(_columns, _line))) for _line in _rt_list]

  # 获取用户信息
  @classmethod
  def get_by_name(cls, username):
    _rt = cls.get_list([('username', username)])
    return _rt[0] if len(_rt) > 0 else None

  # 验证用户名，密码是否正确
  @classmethod
  def validate_add(cls, username , password, age):
    if username.strip() == '':
      return False,u'用户名不能为空'

    #检查用户名是否重复
    if cls.get_by_name(username):
      return False, u'用户名已存在'

    #密码要求长度必须大于等于6
    if len(password) < 6:
      return False, u'密码长度必须大于等于6'

    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
      return False, u'年龄必须是0到100的数字'

    return True, ''

  #添加用户信息
  @classmethod
  def add(cls, username, password, age):
    _sql = 'insert into user (username, password, age) values (%s,md5(%s),%s)'
    _args = (username, password, age)
    MySQLConnection.execute_sql(_sql, _args, False)

  def validate_add2(self):
    _is_ok = True
    _errors = {}

    if self.username.strip() == '':
      _is_ok = False
      _errors['username'] = '用户名不允许为空'

    #检查用户名是否重复
    _user = self.get_by_name(self.username)
    if _user and _user.username == self.username:
      _is_ok = False
      _errors['username'] = '用户名已存在'

    #密码要求长度必须大于等于6
    if len(self.password) < 6:
      _is_ok = False
      _errors['password'] = '密码长度必须大于等于6'

    if not str(self.age).isdigit() or int(self.age) <= 0 or int(self.age) > 100:
      _is_ok = False
      _errors['age'] = '年龄必须是0到100的数字'

    return _is_ok, _errors

  def save(self):
    _sql = 'insert into user (username, password, age) values (%s,md5(%s),%s)'
    _args = (self.username, self.password, self.age)
    MySQLConnection.execute_sql(_sql, _args, False)

  #检查更新用户信息
  @classmethod
  def validate_update(cls, user):
    _is_ok = True
    _errors = {}
    username = user.get('username','')
    age = user.get('age','')

    if cls.get_by_name(username) is None:
      _is_ok = False
      _errors['username'] = '用户信息不存在'

  #  #密码要求长度必须大于等于6
  #  if len(password) < 6:
  #    return False, u'密码长度必须大于等于6'

    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
      _is_ok = False
      _errors['age'] = '年龄必须是0到100的数字'

    return _is_ok, _errors
  
  #更新用户信息
  @classmethod
  def update(cls, user):
    username = user.get('username','')
    age = user.get('age','')
    _sql = 'update user set age=%s where username=%s'
    MySQLConnection.execute_sql(_sql, (age,username), False)

  #删除用户信息
  @classmethod
  def delete(cls , username):
    _sql = 'delete from user where username=%s'
    MySQLConnection.execute_sql(_sql,(username,),False)

  @classmethod
  def validate_change_password(cls, username, upassword, musername, mpassword):
    _is_ok = True
    _errors = {}

    # 检查管理员密码是否争取
    if not cls.validate_login(musername, mpassword):
      _is_ok = False
      _errors['musername'] = '管理员密码错误'

    if cls.get_by_name(username) is None:
      _is_ok = False
      _errors['username'] = '用户信息不存在'

    if len(upassword) < 6:
      _is_ok = False
      _errors['upassword'] = '密码长度必须大于等于6'

    return _is_ok, _errors

  @classmethod
  def change_password(cls, username, upassword):
    _sql = 'update user set password=md5(%s) where username =%s'
    _args = (upassword,username)
    MySQLConnection.execute_sql(_sql, _args, False)

class Performs(object):
  @classmethod
  def add(cls, req):
    _ip = req.get('ip')
    _cpu = req.get('cpu')
    _ram = req.get('ram')
    _time = req.get('time')
    _sql = 'insert into performs(ip, cpu, ram, time)values(%s, %s, %s, %s)';
    MySQLConnection.execute_sql(_sql, (_ip, _cpu, _ram, _time),  False)

  @classmethod
  def get_list(cls, ip):
    _sql = 'SELECT cpu, ram, time FROM performs WHERE ip=%s and time>=%s order by time asc'
    _args = (ip, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() -60*60)))
    _count , _rt_list = MySQLConnection.execute_sql(_sql, _args)
    datetime_list = []
    cpu_list = []
    ram_list = []
    for _cpu, _ram, _time in _rt_list:
      cpu_list.append(_cpu)
      ram_list.append(_ram)
      datetime_list.append(_time.strftime('%H:%M:%S'))
    return datetime_list, cpu_list, ram_list

if __name__ == '__main__':
  pass
