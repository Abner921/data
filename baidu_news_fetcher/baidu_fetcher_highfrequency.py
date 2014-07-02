# -*- coding: utf-8 -*-

import MySQLdb
import urllib
import urllib2
from datetime import datetime
import baidu_news_fetcher
import ftd_common
import time

if __name__ == "__main__":
  while 1:
    print "get keywords"
    lines = ftd_common.get_keywords_by_sql(
    "SELECT t_keywords.id, t_keywords.content_to_search, count(t_keyword_activities.keyword_id) AS c FROM `t_keyword_activities` " + 
    "JOIN t_keywords ON t_keywords.id = t_keyword_activities.keyword_id " + 
    "GROUP BY t_keyword_activities.keyword_id ORDER BY `c`")
    
    for (line) in lines:
      print line[2]
      # fetch when we have less than 2 news
      if line[2] <= 1:
        keyword = line[1]
        print "search " + keyword
        result_list = baidu_news_fetcher.fetchBaiduNews(keyword)
        print result_list
        for result in result_list:
          ftd_common.insert_activity({'keyword_id': line[0], "title": result[1].decode('GBK').encode('UTF-8'), "content": "", "link": result[0], "deleted": 0, "origin": result[2].decode('GBK').encode('UTF-8'), "creation_time": result[3]})
      else:
        print "cancel current loop"
        break

    time.sleep(5)
