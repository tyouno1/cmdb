#encoding:utf-8
from dbutils_class import MySQLConnection
import time
import getip2.database
'''
CREATE TABLE `accesslog` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `logtime` datetime NOT NULL,
  `ip` varchar(128) NOT NULL,
  `url` varchar(20) NOT NULL,
  `status` int NOT NULL,
  `lat` float NOT NULL,
  `lng` float NOT NULL,
  `city` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
def log2db(logfile):
  reader = geoip2.database.Reader('GeoLite2-City.mmdb')
  fhandler = open(logfile,'r')
  rt_list = []
  #统计
  while True:
    line = fhandler.readline()
    if line=='':
      break
    nodes = line.split()
    ip , logtime , url, status  = nodes[0], nodes[3], nodes[6] , nodes[8]
    logtime = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(logtime,'%d/%b/%Y:%H:%M:%S')) 
    try:
      reponse = reader.city(ip)
      if 'China' != reponse.country.name:
        print 'ip not in china %s' % ip
        continue
      city = reponse.city.names.get('zh-CN','')
      if city == '':
        print "ip city is empty:%s" % ip
        continue
      lat = reponse.location.latitude 
      lng = reponse.location.longitude
      rt_list.append((ip, logtime, url, status, lat, lng, city))
    except BaseException as e:
      print 'geo ip not found ip %s' % ip

  fhandler.close()
  reader.close()

  _sql = 'insert into accesslog2(logtime, ip , url, status, lat, lng, city) values (%s,%s,%s,%s,%s,%s,%s)'
  MySQLConnection.bulker_commit_sql(_sql,rt_list)

if __name__ == '__main__':
  log2db('access.log')
