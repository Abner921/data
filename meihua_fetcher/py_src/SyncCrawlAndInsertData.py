#!/usr/bin/env python
# -*- coding: utf-8 -*-


from multiprocessing import Pool,Manager
from SingleActionProcessor import *
from MeihuaDataParser import *
from MeihuaDataWriter import *

parser = MeihuaDataParser()
writer = MeihuaDataWriter()

def creatAndStartPool (cookielists,actionList):
  # set the processes max number 6
  pool = Pool(processes=6)
  """cookielist is created to share data """
  manager = Manager()
  cookielist = manager.list()
  for cookie in cookielists:
    cookielist.append(cookie)
  results = []  #store  return results
  """start subprocess"""
  for action in actionList:
    results.append(pool.apply_async(crawlDataByType, (action,cookielist)))
  #
  pool.close()
  pool.join()
    
  return results
    
def crawlDataByType (action,cookielist):
  print "================== ADTYPE : ", action["url_params"]["adType"]
  """create a SingleActionProcessor object,and put cookie in newActionProcessor"""
  newActionProcessor = SingleActionProcessor()
  for cookie in cookielist:
    newActionProcessor.cj.set_cookie(cookie)
  inputInfo = {}
  returnCode = newActionProcessor.processOneActionWithRetry(inputInfo, action)
  
  if returnCode != ErrorCode.ACTION_SUCCEED:
    utility.printError("Get search result request failed for keyword,the type: " +
                       action['url_params']['adType'] + " errorcode: " + str(returnCode))
    return

  # Parse the data:
  allAdContent = inputInfo["MEIHUA_SEARCH_RESULT"]
  results = parser.parseData(allAdContent)
  results.append(action["url_params"]["adType"])
  
  return results  

def crawlDataByType1 (keyword,adType,crawlParameters,inputInfo,createSqls,keywordId,cookielist,printCreateSql,dbLayer):
  print "================== ADTYPE : ", adType, " kwd: ", keyword
  """create a SingleActionProcessor object,and put cookie in newActionProcessor"""
  newActionProcessor = SingleActionProcessor()
  for cookie in cookielist:
    newActionProcessor.cj.set_cookie(cookie)
    
  crawlParameters['AD_TYPE'] = adType
  listAllAction = copy.deepcopy(MeihuaListAllAction)
  utility.processSiteData(listAllAction, crawlParameters)
  returnCode = newActionProcessor.processOneActionWithRetry(inputInfo, listAllAction)
  
  if returnCode != ErrorCode.ACTION_SUCCEED:
    utility.printError("Get search result request failed for keyword: " +
                       keyword + " errorcode: " + str(returnCode))
    return

  # Parse the data:
  allAdContent = inputInfo["MEIHUA_SEARCH_RESULT"]
  results = parser.parseData(allAdContent)
  
  if printCreateSql and len(results) > 0:
    createSql = writer.getCreateTableSql(results, adType)
    createSqls.append(createSql)
    createSqls.append("")
  
  if not printCreateSql and len(results) > 0:
    print "Inserting ", len(results), " records."
    writer.insertToTable(dbLayer, keywordId, results, adType)
    
    
    
    
    
    
    