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
  curs.execute(sql)
  return curs.fetchall()

def insert_activity(result):
  link = result["link"]
  curs.execute("SELECT id FROM t_keyword_activities WHERE link = %s", link)
  if curs.fetchone() is None and not testing:
    curs.execute("INSERT t_keyword_activities VALUES (null, %s, %s, %s, %s, %s, %s, %s)",
                 [
                   result["keyword_id"],
                   result["title"],
                   result["content"],
                   result["link"],
                   result["deleted"],
                   result["origin"],
                   result["creation_time"]
                  ])
    conn.commit()

