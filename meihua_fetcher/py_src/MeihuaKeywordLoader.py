#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DatabaseLayer import *;

class MeihuaKeywordLoader:

  def getAllKeywords(self, dbLayer):
    return dbLayer.getRows("select * from t_keywords", True)
  
  def getFrequentKeywords(self, dbLayer):         
    sql = "select * from t_keywords where search_count > 0 order by search_count desc limit 1000"
    return dbLayer.getRows(sql,True)