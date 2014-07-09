#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DatabaseLayer import *;

class MeihuaKeywordLoader:

  def getAllKeywords(self, dbLayer):
    return dbLayer.getRows("select * from t_keywords", True)
  