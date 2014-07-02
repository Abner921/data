#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,urllib,urllib2,gzip,StringIO,io,cookielib,re,socket,time,os,traceback,copy
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

request_info_loader = RequestInfoLoader(utility)
actionProcessor = SingleActionProcessor()
utility = Utility()

def runMeihuaPipeline(keywordList):
  try:
    productFileName = "meihua_config.txt"
    # Return False if failed, or True if done.
    productRequestFilePath = utility.getProductRequestFilePath(productFileName)
    (siteInfo, inputInfo) = request_info_loader.loadAddProductRequestFromFile(productRequestFilePath)
    utility.preFillInput(inputInfo)
    
    inputInfo["USERNAME"] = siteInfo["LOGIN"]["MEIHUA"]["USERNAME"]
    inputInfo["PASSWORD"] = siteInfo["LOGIN"]["MEIHUA"]["PASSWORD"]

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
    
    # Start to fill in the keyword and search:
    for keyword in keywordList:
      searchCookieAction = copy.deepcopy(MeihuaGetSearchCookieAction)
      utility.processSiteData(searchCookieAction, {'KEYWORD' : keyword})
      returnCode = actionProcessor.processOneActionWithRetry(inputInfo, searchCookieAction)
      if returnCode != ErrorCode.ACTION_SUCCEED:
        utility.printError("Get cookie request failed for keyword: " +
                           keyword + " errorcode: " + str(returnCode))
        continue
      
      returnCode = actionProcessor.processOneActionWithRetry(inputInfo, MeihuaListAllAction)

      if returnCode != ErrorCode.ACTION_SUCCEED:
        utility.printError("Get search result request failed for keyword: " +
                           keyword + " errorcode: " + str(returnCode))
        continue
      
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


if __name__ == "__main__":
  runMeihuaPipeline(["万科 "])


#productInput = utility.loadProductFromFile(
#    utility.getConfigureFilePath("test_product.txt"))
#processOneAction(ec21LoginAction, productInput, True)
#processOneAction(ec21SearchCategoryAction, productInput, True)
