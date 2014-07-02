# -*- coding: utf-8 -*-

import MySQLdb
import urllib
import urllib2
from datetime import datetime

conn = MySQLdb.connect(host='127.0.0.1', db='camera', user='root', passwd='', charset='utf8')
curs = conn.cursor()

def get_all_keywords():
  curs.execute("SELECT id, content_to_search FROM t_keywords")
  return curs.fetchall()

def get_keywords_by_sql(sql):
  curs.execute(sql)
  return curs.fetchall()

def insert_activity(result):
  link = result["link"]
  curs.execute("SELECT id FROM t_keyword_activities WHERE link = %s", link)
  if curs.fetchone() is None:
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

