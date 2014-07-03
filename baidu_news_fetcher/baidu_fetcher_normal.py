#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import baidu_news_fetcher
import ftd_common

socket.setdefaulttimeout(10)

if __name__ == "__main__":
  lines = ftd_common.get_all_keywords()
  for (line) in lines:
    keyword = line[1]
    print "search " + keyword
    result_list = baidu_news_fetcher.fetchBaiduNews(keyword)
    print "Inserting result number: " + str(len(result_list))
    for result in result_list:
      ftd_common.insert_activity({
          'keyword_id': line[0],
          "title": result[1].decode('GBK').encode('UTF-8'),
          "content": "",
          "link": result[0],
          "deleted": 0,
          "origin": result[2].decode('GBK').encode('UTF-8'),
          "creation_time": result[3]
      })
      
      
