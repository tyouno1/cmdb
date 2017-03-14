#encoding:utf-8
import dbutils

'''
CREATE TABLE `accesslog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(20) NOT NULL,
  `ip` varchar(128) NOT NULL,
  `code` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
def log2db(logfile):
  fhandler = open(logfile,'r')
  rt_list = []
  _sql = 'insert into accesslog(url,ip,code) values (%s,%s,%s)'
  #统计
  while True:
    line = fhandler.readline()
    if line=='':
      break
    nodes = line.split()
    rt_list.append((nodes[0], nodes[6] , nodes[8]))
  fhandler.close()
  dbutils.bulker_commit_sql(_sql,rt_list)

if __name__ == '__main__':
  log2db('/tmp/nginx-log/example.log')
