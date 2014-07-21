#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,urllib,urllib2,gzip,StringIO,cookielib,re,socket,time
from urllib2 import URLError, HTTPError
from Utility import Utility
from ErrorCode import *
from baidu_news_parser import *

utility = Utility()

# Note: Don't install_opener as a global opener for now, considering
# timeouts. For each batch-send/fetch, we require one explicit login.
# Also, we don't use Basic Auth Handler.
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
parser = BaiduNewsParser()

reload(sys)
sys.setdefaultencoding('utf-8')

def fetchOneUrl(requestUrl):
  requestHeaders = {}
  content = ""
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
    return (ErrorCode.ACTION_RETRY_HTTP_ERROR, str(e))
  except URLError, e:
    utility.printError('We failed to reach a server. Reason: ' + str(e.reason))
    return (ErrorCode.ACTION_RETRY_URL_ERROR, str(e))
  except socket.timeout, e:
    errno, errstr = sys.exc_info()[:2]
    utility.printError("Socket Timeout (1): " + str(errno) + ": " + str(errstr))
    return (ErrorCode.ACTION_RETRY_TIMEOUT, str(e))
  except socket.error, e:
    errno, errstr = sys.exc_info()[:2]
    if errno == socket.timeout:
      utility.printError("Socket Timeout (2): " + str(errno) + ": " + str(errstr))
      return (ErrorCode.ACTION_RETRY_TIMEOUT, str(e))
    else:
      utility.printError("Socket Error: " + str(errno) + ": " + str(errstr))
      return (ErrorCode.ACTION_SOCKET_ERROR, str(e))
  except:
    utility.printError("Unknown Error")
    return (ErrorCode.ACTION_UNKNOWN_ERROR, "")

  # print content
  return (ErrorCode.ACTION_SUCCEED, content)


# newsFeedType: "news", "newsfcu", "newsfc". This can affect crawlling efficiency.
def fetchBaiduNews(keyword, number = "20", isOnlySearchInTitle = True, isSortByTime = True, newsFeedType = "news"):
  if isOnlySearchInTitle:
    keyword = "title:" + keyword

  if isSortByTime:
    ctValue = "0"
  else:
    ctValue = "1"
  
  startIndex = 0;
  
  # cl = 2: no duplication
  # ct = 0：sort by time, ct = 1: sort by relevance
  # tn = nesfcu, news, newsdy
  # rn = 50: records per page
  values = {
    "cl" : "2",
    "ct" : ctValue,
    "from" : "news",
    "pn" : str(startIndex),
    "rn" : str(number),
    "tn" : newsFeedType,
    "word" : keyword
  }

  url = "http://news.baidu.com/ns?" + urllib.urlencode(values)
  
  (result, content) = fetchOneUrl(url)
  if result == ErrorCode.ACTION_SUCCEED:
    news_results = parser.parseBaiduNewsHtml(content, newsFeedType)
    if len(news_results) == 0:
      print "Empty result for keyword: ", keyword, " url: ", url
    return news_results
  else:
    print "Error for keyword: ", keyword, " error: ", str(result), " message: ", content
    return []
    
