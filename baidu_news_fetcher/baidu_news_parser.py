#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
# to use escape / unescape
from xml.sax.saxutils import *

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

    elif newsFeedType == "news":
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

        print "title: ", title
        print "link: ", link
        print "origin: ", origin
        print "time: ", time
        print "picture: ", picture
        print "summary: ", summary

        article_result_list.append({
          "link": unescape(link),
          "title": unescape(title).encode('UTF-8'),
          "origin": unescape(origin).encode('UTF-8'),
          "creation_time": time,
          "picture": unescape(picture),
          "content": unescape(summary).encode('UTF-8')
        })
  
    print article_result_list
    return article_result_list
