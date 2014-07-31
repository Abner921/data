#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ResultData:
  # status indicate whether crawling is success or not.yes/no
  # type indicate that which type we use to crawl data
  # resultMap store value
  def __init__(self):
    self.status = 6
    self.actionInfo = {}
    self.resultMap = {}
  
  def getActionInfo(self):
    return self.actionInfo
  
  def getStatus(self):
    return self.status
  
  def getResultMap(self):
    return self.resultMap
  
  def setActionInfo(self, actionInfo):
    self.actionInfo = actionInfo
    
  def setStatus(self, status):
    self.status = status
    
  def setResultMap(self, resultMap):
    self.resultMap = resultMap