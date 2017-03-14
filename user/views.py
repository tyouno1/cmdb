#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#import os
import json
from functools import wraps
#from flask import Flask,
from flask import render_template,request,redirect, session,flash
import loganalysis
#import user
#import userdb as user
import asset
from models import User

# 导入app
# user 模块下的app变量(Flask对象)
from user import app


#app = Flask(__name__)
## 生成随机32位的KEY, os.urandom(32)
## app.secret_key = '\x11\x1fL\x931M\x16I\x8f\xddR\xc2jk\xe37\xdf\xbd\x8f\xd1\x9c\x9e\x1c\x1c\x89o\xc8\xa7\xf2\xe7H^'
#app.secret_key = os.urandom(32)

def login_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if session.get('user') is None:
      return redirect('/')
    rt = func(*args, **kwargs)
    return rt
  return wrapper

@app.route('/')
def index():
  return render_template('login.html')

@app.route('/logs/')
def logs():
  logfile='/tmp/nginx-log/example.log'
  topn = request.args.get('topn',10)
  topn = int(topn) if str(topn).isdigit() else 10
  rt_list = loganalysis.loganalysis(logfile,topn) 
  return render_template('logs.html',rt_list=rt_list, title='topn log')

@app.route('/login/',methods=['POST','GET'])
def login():
  #request.args ---> GET
  #request.form ---> POST
  params = request.args if request.method == 'GET' else request.form
  username = params.get('username','')
  password = params.get('password','')

  _user = User.validate_login(username, password)
  if _user :
    #return '登录成功'
    #return redirect('/logs/') 
    #return render_template('users.html', user_list=user.get_users())
    session['user'] = _user
    return redirect('/users/')
  else:
    return render_template('login.html',username=username, error='username or password is error.')

#用户列表显示
@app.route('/users/')
@login_required
def users():
  user_list=User.get_list()
  print user_list
  return render_template('users.html', user_list=user_list)

#跳转到新建用户信息输入的页面
@app.route('/user/create/', methods=['POST','GET'])
@login_required
def createuser():
  return render_template('user_create.html') 

#提交新建用户的信息
@app.route('/user/add/', methods=['POST'])
@login_required
def add_user():
  username = request.form.get('username', '')
  password = request.form.get('password', '')
  age = request.form.get('age','')

  _user = User(username=username, password=password, age=age)
  _is_ok, _errors = _user.validate_add2()
  print _errors
  if _is_ok:
    _user.save()

  return json.dumps({'is_ok':_is_ok, "errors":_errors, 'success':'添加成功'})
'''
  #检查用户信息
  _is_ok, _error = User.validate_add(username, password, age)

#  if _is_ok:
#    user.add_user(username, password, age)  # 检查OK，添加用户信息
#    return redirect(url_for('users', msg='新建成功'))
#  else:
#    # 跳转到用户新建页面，回显错误信息&用户信息
#    return render_template('create_user.html', \
#                            error=_error, username=username, \
#                            password=password , age=age)
  if _is_ok:
    User.add(username, password, age)  # 检查OK，添加用户信息
'''

# 用户修改页面
@app.route('/user/modify/',methods=['POST','GET'])
@login_required
def modify_user():
  username = request.args.get('username', '')
  _user = User.get_by_name(username)
  return render_template('user_modify.html', user=_user)

# 提交用户修改数据
@app.route('/user/update/', methods=['POST'])
@login_required
def update_user():
  # 检查用户信息
  _is_ok, _errors = User.validate_update(request.form)

#  if _is_ok:
#    user.update_user(username, password, age)  # 检查OK，添加用户信息
#    flash('修改用户信息成功')
#    return redirect('/users/')
#  else:
#    # 跳转到用户新建页面，回显错误信息&用户信息
#    return render_template('modify_user.html', \
#                            error=_error, username=username, \
#                            password=password , age=age)
  if _is_ok:
    User.update(request.form)  # 检查OK，更新用户信息

  return json.dumps({'is_ok':_is_ok, "error":_errors, "success":"更新成功"})

@app.route('/user/delete/')
@login_required
def delete_user():
  username = request.args.get('username','')
  User.delete(username)
  flash('删除用户信息成功')
  return redirect('/users/')

# 用户修改页面
@app.route('/user/modify-password/',methods=['POST','GET'])
@login_required
def modify_password():
  username = request.args.get('username', '')
  _user = User.get_by_name(username)
  return render_template('user_modify-password.html', user=_user)

@app.route('/user/change-password/', methods=['POST'])
@login_required
def change_user_password():
  username=request.form.get('username')
  manager_password=request.form.get('manager-password')
  user_password=request.form.get('user-password')

  print username, manager_password, user_password,session['user']['username']
  _is_ok, _errors = User.validate_change_password(username, user_password , \
                    session['user']['username'], manager_password)
  if _is_ok:
    User.change_password(username,user_password)

  return json.dumps({'is_ok':_is_ok, "errors":_errors,"success":"更新密码成功"})

@app.route('/logout/')
@login_required
def logout():
  session.clear()
  #session['user']
  print session
  return redirect('/')

@app.route('/test/', methods=['POST','GET'])
def test():
#  gender = request.form.get('gender','1')
#  hobby = request.form.getlist('hobby')
#  img =  request.files.get('img')
#  
#  if img:
#    print img.filename
#    img.save('/tmp/kk.txt')
#  print gender 
#  print hobby
#  print request.form
#  print request.files

  print request.form
  print request.args
  print request.files
  print request.headers
  return render_template('test.html')

#资产列表显示
@app.route('/assets/')
@login_required
def assets():
  _cnt, _assets = asset.get_list()
  return render_template('assets.html', assets=_assets, idcs=asset.get_idc_list())

@app.route('/asset/create/', methods=['POST','GET'])
@login_required
def create_asset():
  return render_template('asset_create.html', idcs=asset.get_idc_list())

@app.route('/asset/add/', methods=['POST'])
@login_required
def add_asset():
  _is_ok , _errors = asset.validate_create(request.form)
  if _is_ok:
    asset.create(request.form)
  return json.dumps({'is_ok':_is_ok, 'errors':_errors, 'success':'添加成功'})

@app.route('/asset/modify/')
@login_required
def modify_asset():
  _id = request.args.get('id','')
  _count, _asset = asset.get_by_id(_id)
  _idcs = asset.get_idc_list()
  return render_template('asset_modify.html', asset=_asset[0], idcs=_idcs)

@app.route('/asset/update/', methods=['POST'])
@login_required
def update_asset():
  _is_ok, _errors = asset.validate_update(request.form)
  if _is_ok:
      asset.update(request.form)
  return json.dumps({'is_ok': _is_ok, 'errors': _errors,'success':'更新成功'})

@app.route('/asset/delete/', methods=['GET'])
@login_required
def delete_asset():
  _id = request.args.get('id','')
  asset.delete(_id)
  return redirect('/assets/')


#if __name__ == '__main__':
#  app.run(host='0.0.0.0', port=9001,debug=True)
