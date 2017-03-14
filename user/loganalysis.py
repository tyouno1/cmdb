#encoding:utf-8

def loganalysis(logfile, topn=10):
  fhandler = open(logfile,'r')
  rt_dict = {}
  #统计
  while True:
    line = fhandler.readline()
    if line=='':
      break
    nodes = line.split()
    ip, url , code = nodes[0], nodes[6], nodes[8]
    key = (ip, url, code)
#    if key not in rt_dict:
#      rt_dict[key] = 1
#    else:
#      rt_dict[key] = rt_dict[key] + 1
    # 简单写法
    rt_dict[key] = rt_dict.get(key,0) + 1
  fhandler.close()

  # 排序
  rt_list = rt_dict.items()
  # [(key,value) (key,value)]
  # 冒泡排序,找出前n个
  for j in range(0, topn):
    for i in range(0, len(rt_list) - 1):
      if rt_list[i][1] > rt_list[i + 1][1]:
        #temp = rt_list[i]
        #rt_list[i] = rt_list[i + 1]
        #rt_list[i + 1] = temp
        # 简单写法
        rt_list[i], rt_list[i+1] = rt_list[i+1] , rt_list[i]

  return rt_list[-1:-topn-1:-1]

if __name__ == '__main__':
  print loganalysis('/tmp/nginx-log/example.log')
