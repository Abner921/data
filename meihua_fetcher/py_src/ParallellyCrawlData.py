#!/usr/bin/env python
# -*- coding: utf-8 -*-


from multiprocessing import Pool,Manager
from SingleActionProcessor import *
from MeihuaDataParser import *
from MeihuaDataWriter import *
from ResultData import *

# coolieLists store coolie that we can use to login page 
# actionList store some things we will to do 
# processCount is the number of process
def creatAndStartPool (cookielists,actionList,processCount):
  # set the processes max number processCount
  pool = Pool(processes=int(processCount))
  # cookieList is created to share data with other process
  manager = Manager()
  cookielist = manager.list()
  for cookie in cookielists:
    cookielist.append(cookie)
  # store  return results
  results = []  
  # start subprocess
  for action in actionList:
    results.append(pool.apply_async(processActionsParallelly, (action,cookielist)))
  pool.close()
  pool.join()
    
  return results
    
def processActionsParallelly(action,cookielist):
  # create a SingleActionProcessor object,and put cookie in newActionProcessor
  newActionProcessor = SingleActionProcessor()
  newActionProcessor.setCookie(cookielist)
  # store content that webPage return
  inputInfo = {}
  resultData = ResultData()
  returnCode = newActionProcessor.processOneActionWithRetry(inputInfo, action)
  
  if returnCode != ErrorCode.ACTION_SUCCEED:
    utility.printError("Get search result request failed for this action: " +
                       action['action_name'] + " errorcode: " + str(returnCode))
    return resultData
  
  #define a list to store results
  results = {}
  # resultMap store some keys,and we need these keys to obtain results 
  resultMap = action["result"][0]
  #print resultMap.items()
  for (key,value) in resultMap.items():
    if key == 'result_regex': continue
    if key == 'match_multiline': continue
    results[value] = inputInfo[value]
    
  # Parse the data:
  # allAdContent = inputInfo["MEIHUA_SEARCH_RESULT"]
  # results = parser.parseData(allAdContent)
  adType = action["url_params"]["adType"]
  if results:
    resultData.setResultMap(results)
    resultData.setStatus("yes")
    resultData.setType(adType)
  
  return resultData  

    
    
    
    
    
    
    