# -*- coding: utf-8 -*-

import MySQLdb
from urllib import urlencode
from urlparse import urlparse, parse_qs, urlunparse

ENV = "development"

def get_db_conn(environment = "development"):
  if environment == "development":
    return MySQLdb.connect(host='127.0.0.1', db='fdd_direct', user='root', passwd='', charset='utf8')
  elif environment == "staging":
    return MySQLdb.connect(host='114.215.200.214', db='fdd_direct', user='root', passwd='', charset='utf8', port=33306)
  elif environment == "production":
    return MySQLdb.connect(host='192.168.222.90', db='fdd_direct', user='admin', passwd='Admin_12345', charset='utf8')
  else:
    return None

conn = get_db_conn(ENV)

print "Database connected."

curs = conn.cursor()
testing = False

def get_all_keywords():
  curs.execute("SELECT id, content_to_search FROM t_keywords")
  return curs.fetchall()

def get_keywords_by_sql(sql):
  conn2 = get_db_conn(ENV)
  curs2 = conn2.cursor()
  curs2.execute(sql)
  result = curs2.fetchall()
  curs2.close()
  conn2.close()
  return result

def update_by_sql(sql):
  curs.execute(sql)
  conn.commit()

def close_conn():
  curs.close()
  conn.close()

def insert_activity(keyword_id, result):
  link = remove_gabage_params(result["link"])
  conn3 = get_db_conn(ENV)
  curs3 = conn3.cursor()
  
  # check title to prevent duplicate news from different websites
  if result["title"]:
    curs3.execute("SELECT id FROM t_keyword_activities WHERE link = %s OR title = %s", [link, result["title"]])
  else:
    curs3.execute("SELECT id FROM t_keyword_activities WHERE link = %s", [link])

  if curs3.fetchone() is None and not testing:
    curs3.execute("INSERT t_keyword_activities VALUES (null, %s, %s, %s, %s, %s, %s, %s, %s)",
                 [
                   keyword_id,
                   result["title"],
                   result["content"],
                   result["link"],
                   0,  # deleted
                   result["origin"],
                   result["creation_time"],
                   result["picture"]
                  ])
    conn3.commit()
    curs3.close()
    conn3.close()


# turn http://yn.house.sina.com.cn/scan/2014-07-14/11044289383.shtml?wt_source=data8_lpdt00_bt01
# into http://yn.house.sina.com.cn/scan/2014-07-14/11044289383.shtml
def remove_gabage_params(url):
  parsed = urlparse(url)
  qd = parse_qs(parsed.query, keep_blank_values=True)
  filtered = dict((k, v) for k, v in qd.iteritems() if not k.startswith('wt_'))
  newurl = urlunparse([
      parsed.scheme,
      parsed.netloc,
      parsed.path,
      parsed.params,
      urlencode(filtered, doseq=True), # query string
      parsed.fragment
  ])
  return newurl


