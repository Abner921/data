#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DatabaseLayer import *;

class MeihuaKeywordLoader:

  def getAllKeywords(self, dbLayer):
    return dbLayer.getRows("select * from t_keywords", True)
  
  def getFrequentKeywords(self, dbLayer):
    sql = "SELECT t_keywords.id, t_keywords.content_to_display, t_keywords.content_to_search, t_keywords.search_count, count(t_keyword_activities.keyword_id) AS c FROM t_keywords \
           LEFT JOIN t_keyword_activities ON t_keywords.id = t_keyword_activities.keyword_id \
          WHERE t_keywords.search_count = 0 GROUP BY t_keyword_activities.keyword_id, t_keywords.id HAVING c <=0"     
    return dbLayer.getRows(sql,True)