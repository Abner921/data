#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,urllib,urllib2,gzip,StringIO,io,cookielib,re,socket,time,os,traceback,copy
from cookielib import CookieJar
from threading import Thread
import socket
from urllib2 import Request, urlopen, URLError, HTTPError
from Utility import Utility
from ErrorCode import *
import MySQLdb
import sys

TIMEOUTS = 50
utility = Utility()
socket.setdefaulttimeout(TIMEOUTS)

# Note: Don't install_opener as a global opener for now, considering
# timeouts. For each batch-send/fetch, we require one explicit login.
# Also, we don't use Basic Auth Handler.
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

conn = MySQLdb.connect(host='127.0.0.1', db='camera', user='root', passwd='', charset='utf8')
curs = conn.cursor()

reload(sys)
sys.setdefaultencoding('utf-8')

def fetchOneUrl(requestUrl):
  requestHeaders = {}
  request = urllib2.Request(
      url = requestUrl,
      headers = requestHeaders)

  try:
    response = urllib2.urlopen(request)

    if response.info().get('Content-Encoding') and response.info().get('Content-Encoding').find('gzip') >= 0:
      utility.printMessage('gzip enabled: suggest to remove the Content-Encoding setting!')
      buf = StringIO.StringIO(response.read())
      gzipFile = gzip.GzipFile(fileobj=buf)
      content = gzipFile.read()
    else:
      content = response.read()

  except HTTPError, e:
    utility.printError('The server couldn\'t fulfill the request. Error code: ' + str(e.code))
    return ErrorCode.ACTION_RETRY_HTTP_ERROR
  except URLError, e:
    utility.printError('We failed to reach a server. Reason: ' + str(e.reason))
    return ErrorCode.ACTION_RETRY_URL_ERROR
  except socket.timeout, e:
    errno, errstr = sys.exc_info()[:2]
    utility.printError("Socket Timeout (1): " + errno + ": " + errstr)
    return ErrorCode.ACTION_RETRY_TIMEOUT
  except socket.error, e:
    errno, errstr = sys.exc_info()[:2]
    if errno == socket.timeout:
      utility.printError("Socket Timeout (2): " + errno + ": " + errstr)
      return ErrorCode.ACTION_RETRY_TIMEOUT
    else:
      utility.printError("Socket Error: " + errno + ": " + errstr)
      return ErrorCode.ACTION_SOCKET_ERROR
  
  # print content
  return content


def getRegexMatcher(regPattern):
  """
  
  Note:
  re.S:.match any char including newline
  re.M:^$ match each line instead of the first line.
  >>> re.findall(r"^a(\d+)b", "a23b\na34b", re.M)
          ['23', '34']
  """
  caseSensitive = True
  matchMultiline = False
  regex_flag = 0
  if not caseSensitive:
    regex_flag = re.IGNORECASE
  if matchMultiline:
    regex_flag = regex_flag | re.S

  return re.compile(regPattern, regex_flag)


def parseBaiduNewsHtml(html_string, keyword):
  articlelist_regex = getRegexMatcher('class=baidu>.*?<div')
  articlelist_matches = articlelist_regex.findall(html_string)

  if len(articlelist_matches) == 0:
    return []

  articlelist_string = articlelist_matches[0]
  # print "articlelist_string: ", articlelist_string
  article_link_regex = getRegexMatcher('<a href="(.*?)"')
  article_title_regex = getRegexMatcher('target="_blank">(.*?)</a>&nbsp;')
  article_source_regex = getRegexMatcher('<span>(.*?)&nbsp;')
  article_time_regex = getRegexMatcher('<span>.*?&nbsp;(.*?)</span><br>')

  article_link_matches = article_link_regex.findall(articlelist_string)
  article_title_matches = article_title_regex.findall(articlelist_string)
  article_source_matches = article_source_regex.findall(articlelist_string)
  article_time_matches = article_time_regex.findall(articlelist_string)
  
  article_result_list = []
  for link in article_link_matches:
    title = article_title_matches[0]
    source = article_source_matches[0]
    time = article_time_matches[0]
    # print keyword.strip().encode("gb2312"),"|",link,"|",title,"|",source,"|",time
    del article_title_matches[0]
    del article_source_matches[0]
    del article_time_matches[0]
    
    article_result_list.append([link, title, source, time])

  #print article_result_list
  return article_result_list

def insertBaiduResult(keyword_id, result):
  link = result[0]
  curs.execute("SELECT id FROM t_keyword_activities WHERE link = %s", link)
  if curs.fetchone() is None:
    curs.execute("INSERT t_keyword_activities VALUES (null, %s, %s, %s, %s, 0, %s, %s)",
                 [
                   keyword_id,
                   result[1].decode('GBK').encode('UTF-8'),
                   "",
                   result[0],
                   result[2].decode('GBK').encode('UTF-8'),
                   result[3]
                  ])
    conn.commit()

def fetchBaiduNews(keyword):
  values = {"word" : "title:" + keyword}
  url = "http://news.baidu.com/ns?" + urllib.urlencode(values) + "&tn=newsfcu&from=news&cl=2&rn=3&ct=0"
  content = fetchOneUrl(url)
  # TDOO: handle errors
  return parseBaiduNewsHtml(content, keyword)


if __name__ == "__main__":
#  f = open("list.txt")
#  for line in f:
  curs.execute("SELECT id, content_to_search FROM t_keywords")
  for (line) in curs.fetchall():
    keyword = line[1]
    result_list = fetchBaiduNews(keyword)
    for result in result_list:
      insertBaiduResult(line[0], result)
    
