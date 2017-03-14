#encoding: utf-8
import time
from functools import wraps

'''
记录每个函数执行的时间
'''
def time_wrapper(func):
  @wraps(func)
  def wrapper():
    print '计时开始: %s' % func.__name__
    start = time.time()
    rt = func()
    exec_time = time.time() - start
    print '计时结束: %s: %s' % (func.__name__, exec_time)
    return rt 
  return wrapper


'''
记录日志
'''
def logger_wrapper(func):
  @wraps(func)
  def wrapper():
    print '日志记录开始: %s' % func.__name__
    start = time.time()
    rt = func()
    exec_time = time.time() - start
    print '日志记录结束: %s: %s' % (func.__name__, exec_time)
    return rt 
  return wrapper

@logger_wrapper
def test1():
  print 'test1'

@time_wrapper
def test2():
  print 'test2'

def test3():
  print 'test3'

@logger_wrapper
@time_wrapper
def test4():
  time.sleep(2)
  print 'test4'

@time_wrapper
@logger_wrapper
def test5():
  time.sleep(2)
  print 'test5'


'''
在函数之前执行一块代码
在函数之后执行一块代码
'''

def wrapper(func):
  print '执行之前:%s' % func.__name__
  rt = func()
  print '执行之后:%s' % func.__name__
  return rt


'''
print wrapper(test1)
print wrapper(test2)
print wrapper(test3)
print wrapper(test4)
print wrapper(test5)
'''
test1()
test2()
test3()
test4()
test5()
