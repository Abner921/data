#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ResultData:
  # status indicate whether crawling is success or not.yes/no
  # type indicate that which type we use to crawl data
  # resultMap store value
  def __init__(self):
    self.status = "no"
    self.adType = ""
    self.resultMap = {}
  
  def getType(self):
    return self.adType
  
  def getStatus(self):
    return self.status
  
  def getResultMap(self):
    return self.resultMap
  
  def setType(self,adType):
    self.adType = adType
    
  def setStatus(self,status):
    self.status = status
    
  def setResultMap(self,resultMap):
    self.resultMap = resultMap