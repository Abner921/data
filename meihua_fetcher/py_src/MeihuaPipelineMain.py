#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,urllib,urllib2,gzip,StringIO,io,cookielib,re,socket,time,os,traceback,copy,getopt
from cookielib import CookieJar
from threading import Thread
import socket
from urllib2 import Request, urlopen, URLError, HTTPError
from Utility import Utility
from RequestInfoLoader import *
from SingleActionProcessor import *
from SiteData import *
from ErrorCode import *
from SiteDataMeihua import *
from MeihuaKeywordLoader import *
from MeihuaDataParser import *
from MeihuaAdType import *
from MeihuaDataWriter import *
from multiprocessing import Pool,Manager
import datetime

startTime = datetime.datetime.now()
requestInfoLoader = RequestInfoLoader(utility)
actionProcessor = SingleActionProcessor()
utility = Utility()
parser = MeihuaDataParser()
writer = MeihuaDataWriter()
useLocalDb = True
printCreateSql = False
useBrandNameAsKeyword = True  # otherwise use content_to_search
dbDryRunMode = False
outputCrawlerDebugInfo = False

def runMeihuaPipeline(dbLayer, keywordList, startDate, endDate, number, processCount, typeList):
  try:
    productFileName = "meihua_config.txt"
    # Return False if failed, or True if done.
    productRequestFilePath = utility.getProductRequestFilePath(productFileName)
    (siteInfo, inputInfo) = requestInfoLoader.loadAddProductRequestFromFile(productRequestFilePath)
    utility.preFillInput(inputInfo)
    
    inputInfo["USERNAME"] = siteInfo["LOGIN"]["MEIHUA"]["USERNAME"]
    inputInfo["PASSWORD"] = siteInfo["LOGIN"]["MEIHUA"]["PASSWORD"]
    
    if outputCrawlerDebugInfo:
      inputInfo["DEBUG"] = 1

    returnCode = actionProcessor.processOneActionWithRetry(inputInfo, MeihuaLogin1Action)
    if returnCode != ErrorCode.ACTION_SUCCEED:
      utility.printError("Login1 request failed.")
      utility.saveLogFile(productRequestFilePath)
      return returnCode
    
    returnCode = actionProcessor.processOneActionWithRetry(inputInfo, MeihuaLogin2Action)
    if returnCode != ErrorCode.ACTION_SUCCEED:
      utility.printError("Login2 request failed.")
      utility.saveLogFile(productRequestFilePath)
      return returnCode
    
    """
    returnCode = actionProcessor.processOneActionWithRetry(inputInfo, MeihuaLogin3Action)
    if returnCode != ErrorCode.ACTION_SUCCEED:
      utility.printError("Login3 request failed.")
      utility.saveLogFile(productRequestFilePath)
      return returnCode
    """
    
    createSqls = [writer.getCreateSchemaTableSql()]
    
    # Start to fill in the keyword and search:
    progress = 0
    totalProgress = len(keywordList)
    
    for keywordTuple in keywordList:
      print "===== Current progress: ", progress/totalProgress
      print "===== Completed: ", progress, " out of ", totalProgress
      print "===== Current Keyword: ", keywordTuple
      progress = progress + 1

#      print "Keyword: ", keyword[0], " ", keyword[1].encode('UTF-8')
      keywordId = keywordTuple[0]
      if useBrandNameAsKeyword:
        keyword = keywordTuple[1].encode('UTF-8')
      else:
        keyword = keywordTuple[2].encode('UTF-8')

      crawlParameters = {
          'KEYWORD' : keyword,
          'START_DATE' : startDate,
          'END_DATE' : endDate,
          'NUMBER_AD' : number
      }
      searchCookieAction = copy.deepcopy(MeihuaGetSearchCookieAction)
      utility.processSiteData(searchCookieAction, crawlParameters)
      returnCode = actionProcessor.processOneActionWithRetry(inputInfo, searchCookieAction)
      if returnCode != ErrorCode.ACTION_SUCCEED:
        utility.printError("Get cookie request failed for keyword: " +
                           keyword + " errorcode: " + str(returnCode))
        continue
      
      # create a list to store Action
      actionList = []
      for adType in typeList:
        crawlParameters['AD_TYPE'] = adType
        listAllAction = copy.deepcopy(MeihuaListAllAction)
        utility.processSiteData(listAllAction, crawlParameters)
        actionList.append(listAllAction)
      
      # start new process,and crawl data
      results = processActionsParallelly(actionProcessor, actionList, processCount)
        
      for result in results:
        if int(processCount) > 1 and result.get().getStatus() == ErrorCode.ACTION_SUCCEED:
          insertToTableByType(createSqls, keywordId, result.get(), keywordTuple[3])
        elif processCount == "1" and result.getStatus() == ErrorCode.ACTION_SUCCEED:
          insertToTableByType(createSqls, keywordId, result, keywordTuple[3])
    
    print "\n".join(createSqls)
    endTime = datetime.datetime.now()
    print "==============================================================="
    print "start time : ", startTime
    print "spend time : ", endTime - startTime
    print "end   time : ", endTime
    print "==============================================================="
    
  except Exception, e:
    # utility.printError("Un-catched Exceptions when processing request: " +  productFileName, e)
    utility.printError("This request is marked as failed.", e)
    traceback.print_exc(file=utility.logStream)
    traceback.print_exc(file=sys.stdout)
    utility.saveLogFile(productRequestFilePath)

  utility.saveLogFile(productRequestFilePath)

  # add product request file name should be like:
  # add_time_productname.txt
  # datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  
def insertToTableByType(createSqls,keywordId,result, count):
  allAdContent = result.getResultMap()["MEIHUA_SEARCH_RESULT"]
  adType = result.getActionInfo()["url_params"]["adType"]
  value = parser.parseData(allAdContent)
  if printCreateSql and len(value) > 0:
    createSql = writer.getCreateTableSql(value, adType)
    createSqls.append(createSql)
    createSqls.append("")
  
  if not printCreateSql and len(value) > 0:
    print "Inserting ", len(value), " records."
    writer.insertToTable(dbLayer, keywordId, value, adType)
    dbLayer.update_by_sql("UPDATE t_keywords SET search_count = %s WHERE id = %s" % (count + 1, keywordId))


if __name__ == "__main__":
  opts, args = getopt.getopt(sys.argv[1:], "p:s:e:a:n:r:o:cvf",
                             ["password=", "start_date=", "end_date=", "number=", "ad_types=",
                              "remotedb_mode=","processCount=","create_mode", "verbose_mode", "frequent_mode"])
  
  # default values
  start_date = datetime.datetime.now().strftime("%Y-%m-%d")
  end_date= (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
  # MAGAZINE = "1", TV = "2", OUTDOOR = "3", ONLINE = "4", PROMOTION = "5", RADIO = "6"
  ad_types = "1,2,3,4,5,6"
  number = 100
  password = ""
  ip = ""
  processCount = 6
  frequentMode = False

  for op, value in opts:
    if op == "-p" or op == "--password":
      password = value
    elif op == "-s" or op == "--start_date":
      start_date = value
    elif op == "-e" or op == "--end_date":
      end_date = value
    elif op == "-n" or op == "--number":
      number = value
    elif op == "-a" or op == "--ad_types":
      ad_types = value
    elif op == "-c" or op == "--create_mode":
      printCreateSql = True
    elif op == "-r" or op == "--remotedb_mode":
      useLocalDb = False
      ip = value
    elif op == "-v" or op == "--verbose_mode":
      outputCrawlerDebugInfo = True
    elif op == "-o" or op == "--processCount":
      processCount = value
    elif op == "-f" or op == "--frequent_mode":
      frequentMode = True
    else:
      print "Usage: "
      print "MeihuaPipelineMain.py -p pass -s 2013-01-02 -e 2014-02-03 -a 1,2,3 -n 100 -r 114.215.200.214 -o 6 -c -v -f"
      print "MeihuaPipelineMain.py --password=test --start_date=2013-01-02 --end_date=2014-02-03 --ad_types=1,2,3 --remotedb_mode=114.215.200.214"
      print "                      --number=100 --processCount=6 --create_mode --verbose_mode --frequent_mode"
      sys.exit()

  print "outputCrawlerDebugInfo :",outputCrawlerDebugInfo
  print "Is Create Mode: ", printCreateSql
  print "Start: ", start_date
  print "End: ", end_date
  print "Number: ", number
  print "Ad types: ", ad_types
  print "host ip: " , ip
  print "processCount: ", processCount
  print "frequentMode: ", frequentMode

  dbLayer = DatabaseLayer()
  dbLayer.setDryRun(dbDryRunMode)
  if useLocalDb:
    result = dbLayer.connect(host='localhost', db='fdd_direct', user='root', pwd=password)
  else:
    result = dbLayer.connect(host= ip, db='fdd_direct', user='root', pwd=password, dbport=33306)

  if not result:
    exit(1)
  
  loader = MeihuaKeywordLoader()
  if printCreateSql:
    # Use a common keyword to get all schema
    keywords = [[0, u"万科", u"万科"]]
  else:
    print "Loading keywords from database."
    if frequentMode:
      keywords = loader.getFrequentKeywords(dbLayer)
      print len(keywords)
    else:
      keywords = loader.getAllKeywords(dbLayer)
    print "keywords: ", keywords

  runMeihuaPipeline(dbLayer, keywords, start_date, end_date, number,processCount, ad_types.split(","))

  dbLayer.close()
