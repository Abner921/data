#!/usr/bin/env python

# -*- coding: unicode -*-
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

request_info_loader = RequestInfoLoader(utility)
actionProcessor = SingleActionProcessor()

class SingleOperationProcessor:
    
  def processOneOperation(self, inputObjectInfo, siteInfo, operations):
    returnCode = None
    # deal with each site
    for site in siteInfo["SITES"]:
      # For different operations, the input info will not be shared.
      # And within one operation, the input info should be shared.
      inputInfo = copy.deepcopy(inputObjectInfo)
      inputInfo["USERNAME"] = siteInfo["LOGIN"][site]["USERNAME"]
      inputInfo["PASSWORD"] = siteInfo["LOGIN"][site]["PASSWORD"]
      utility.printMessage("==================== " + site + " ====================")
  
      if not operations.has_key(site):
        utility.printError("Invalid action site: " + site)
        continue
  
      # deal with each action
      actions = operations[site]
      for actionInfo in actions:
        utility.printMessage("-------------------")
        returnCode = actionProcessor.processOneActionWithRetry(inputInfo, actionInfo)
    
    return returnCode


  def processOneOperationFromFile(self, productFileName):
    try:
      # Return False if failed, or True if done.
      productRequestFilePath = utility.getProductRequestFilePath(productFileName)
      (siteInfo, productInput) = request_info_loader.loadAddProductRequestFromFile(productRequestFilePath)
      utility.preFillInput(productInput)
      returnCode = self.processOneOperation(productInput, siteInfo, ALL_OPERATIONS)
  
      if returnCode == ErrorCode.ACTION_SUCCEED:
        utility.markProductRequestAsFinished(productFileName)
      else:  
        utility.markProductRequestAsFailed(productFileName)
  
    except Exception, e:
      # utility.printError("Un-catched Exceptions when processing request: " +  productFileName, e)
      utility.printError("This request is marked as failed.", e)
      traceback.print_exc(file=utility.logStream)
      traceback.print_exc(file=sys.stdout)
      utility.markProductRequestAsFailed(productFileName)
      utility.saveLogFile(productRequestFilePath)
  
  
  def loopProcessAddProductRequests(self):
    # list all the product request file:
    while True:
      dirList = os.listdir(utility.getProductRequestPath())
      for fname in dirList:
        if os.path.isdir(fname):
          continue
        if not fname.startswith("add_") or not fname.endswith(".txt") or fname.find("_log") >= 0:
          continue
        
        utility.printMessage(">>>>>>> Processing add-product-request: " + fname + " <<<<<<<<")
        #processAddProductOperation(fname)
        self.processOneOperationFromFile(fname)
  
      print "Sleep 2 seconds before continue. To stop press ctrl+c."
      time.sleep(2)
  
      # add product request file name should be like:
      # add_time_productname.txt
      # datetime.datetime.now().strftime("%Y%m%d%H%M%S")

if __name__ == "__main__":
  singleOperationProcessor = SingleOperationProcessor()
  singleOperationProcessor.loopProcessAddProductRequests()

#productInput = utility.loadProductFromFile(
#    utility.getConfigureFilePath("test_product.txt"))
#processOneAction(ec21LoginAction, productInput, True)
#processOneAction(ec21SearchCategoryAction, productInput, True)
