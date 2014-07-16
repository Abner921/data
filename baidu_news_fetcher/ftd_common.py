# -*- coding: utf-8 -*-

import MySQLdb
#conn = MySQLdb.connect(host='114.215.200.214', db='fdd_direct', user='root', passwd='', charset='utf8', port=33306)
conn = MySQLdb.connect(host='localhost', db='fdd_direct', user='root', passwd='password', charset='utf8')

print "Database connected."

curs = conn.cursor()
testing = False

def get_all_keywords():
  curs.execute("SELECT id, content_to_search FROM t_keywords")
  return curs.fetchall()

def get_keywords_by_sql(sql):
  conn2 = MySQLdb.connect(host='localhost', db='fdd_direct', user='root', passwd='password', charset='utf8')
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
  link = result["link"]
  curs.execute("SELECT id FROM t_keyword_activities WHERE link = %s", link)
  if curs.fetchone() is None and not testing:
    curs.execute("INSERT t_keyword_activities VALUES (null, %s, %s, %s, %s, %s, %s, %s, %s)",
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
    conn.commit()

