#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
# to use escape / unescape
from HTMLParser import *

class BaiduNewsParser:

  def getRegexMatcher(self, regPattern):
    """
    
    Note:
    re.S:.match any char including newline
    re.M:^$ match each line instead of the first line.
    >>> re.findall(r"^a(\d+)b", "a23b\na34b", re.M)
            ['23', '34']
    """
    caseSensitive = True
    matchMultiline = True
    regex_flag = 0
    if not caseSensitive:
      regex_flag = re.IGNORECASE
    if matchMultiline:
      regex_flag = regex_flag | re.S
  
    return re.compile(regPattern, regex_flag)


  def getFormattedOnlyMatch(self, content, regPattern):
    regex = self.getRegexMatcher(regPattern)
    results = regex.findall(content)
    if len(results) >= 1:
      return re.sub("<.*?>", "", results[0].strip(" "))
    else:
      return ""

  
  def parseBaiduNewsHtml(self, html_string, newsFeedType):
    article_result_list = []
    
    if newsFeedType == "newsfcu":
      article_result_list = self.parseBaiduNewsJsonResponse(html_string)

    elif newsFeedType == "news":
      article_result_list = self.parseBaiduNewsHtmlResponse(html_string)
      
    self.formatNewsResponse(article_result_list)
    
    for article in article_result_list:
      print "---------------"
      print "title: ", article["title"]
      print "link: ", article["link"]
      print "origin: ", article["origin"]
      print "time: ", article["creation_time"]
      print "picture: ", article["picture"]
      print "content: ", article["content"]

    return article_result_list


  def parseBaiduNewsJsonResponse(self, html_string):
    article_result_list = []
    articlelist_regex = self.getRegexMatcher('class=baidu>.*?<div')
    articlelist_matches = articlelist_regex.findall(html_string)
  
    if len(articlelist_matches) == 0:
      return []

    articlelist_string = articlelist_matches[0]
    # print "articlelist_string: ", articlelist_string
    article_link_regex = self.getRegexMatcher('<a href="(.*?)"')
    article_title_regex = self.getRegexMatcher('target="_blank">(.*?)</a>&nbsp;')
    article_source_regex = self.getRegexMatcher('<span>(.*?)&nbsp;')
    article_time_regex = self.getRegexMatcher('<span>.*?&nbsp;(.*?)</span><br>')
  
    article_link_matches = article_link_regex.findall(articlelist_string)
    article_title_matches = article_title_regex.findall(articlelist_string)
    article_source_matches = article_source_regex.findall(articlelist_string)
    article_time_matches = article_time_regex.findall(articlelist_string)
  
    for link in article_link_matches:
      title = article_title_matches[0]
      origin = article_source_matches[0]
      time = article_time_matches[0]
      # print keyword.strip().encode("gb2312"),"|",link,"|",title,"|",source,"|",time

      article_result_list.append({
        "link": link,
        "title": title.decode('GBK').encode('UTF-8'),
        "origin": origin.decode('GBK').encode('UTF-8'),
        "creation_time": time,
        "picture": "",
        "content": ""
      })
      del article_title_matches[0]
      del article_source_matches[0]
      del article_time_matches[0]
    
    return article_result_list
  
  def parseBaiduNewsHtmlResponse(self, html_string):
    article_result_list = []
    # here we start to parse the html snippet:
    #'<div id=\"content_left\">.*?<ul>(.*?)</ul></div>'
    
    articlelist_regex = self.getRegexMatcher('<li class=\"result\" id=.*?>(.*?)</li>')
    articlelist_matches = articlelist_regex.findall(html_string)
  
    if len(articlelist_matches) == 0:
      return [] 
    
    for articlelist_string in articlelist_matches:
      link = self.getFormattedOnlyMatch(articlelist_string, '<h3 class="c-title"><a href="(.*?)"')
      title = self.getFormattedOnlyMatch(articlelist_string, '<h3 class="c-title"><a href=.*?>(.*?)</a></h3>')
      origin = self.getFormattedOnlyMatch(articlelist_string, '<span class="c-author">&nbsp;(.*?)&nbsp;.*</span>')
      time = self.getFormattedOnlyMatch(articlelist_string, '<span class="c-author">&nbsp;.*?&nbsp;(.*)</span>')
      picture = self.getFormattedOnlyMatch(articlelist_string, '<a class="c_photo" .*?><img src="(.*?)"')
      summary = self.getFormattedOnlyMatch(articlelist_string, '<div class="c-summary"><a class="c_photo" .*?</a>(.*?)&nbsp;<')
      if summary == "":
        summary = self.getFormattedOnlyMatch(articlelist_string, '<div class="c-summary">(.*?)&nbsp;<')

      article_result_list.append({
        "link": HTMLParser().unescape(link),
        "title": HTMLParser().unescape(title).encode('UTF-8'),
        "origin": HTMLParser().unescape(origin).encode('UTF-8'),
        "creation_time": time,
        "picture": HTMLParser().unescape(picture),
        "content": HTMLParser().unescape(summary).encode('UTF-8')
      })

    return article_result_list


  # list of article results with link/title/origin/creation_time/picture/content
  def formatNewsResponse(self, article_result_list):
    # update the result in place.
    for article in article_result_list:
      article["title"] = self.formatHtmlString(article["title"])
      article["content"] = self.formatHtmlString(article["content"])


  def formatHtmlString(self, html):
    double_unescaped_html = html # HTMLParser().unescape(html)
    TRIM_HEAD_LIST = ["> ", "| ", ","]
    # don't use unicode. use utf-8:
    TRIM_TAIL_LIST = ["(组图)", "(图)"]
    
    # Here we trim some trivia headers:
    for trim_head in TRIM_HEAD_LIST:
      if double_unescaped_html.startswith(trim_head):
        double_unescaped_html = double_unescaped_html[len(trim_head):]

    for trim_tail in TRIM_TAIL_LIST:
      if double_unescaped_html.endswith(trim_tail):
        double_unescaped_html = double_unescaped_html[:len(double_unescaped_html) - len(trim_tail)]

    return double_unescaped_html

