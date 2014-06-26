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

def processOneOperation(inputObjectInfo, siteInfo, operations):
  returnCode = None
  # deal with each site
  for site in siteInfo["SITES"]:
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

      retryTimes = 3
      returnCode = actionProcessor.processOneAction(actionInfo, inputInfo, inputInfo.has_key("DEBUG"))

      backupData = backupFallbackDataForAction(inputInfo, actionInfo)
      # Give it a couple retries for timeout or no-result-fallback.
      # Should only rety for timeout, or unknown reason, or explicitly retry request.
      # For login failure and other cases we should just fail fast.
      while (actionProcessor.shouldRetry(returnCode) and retryTimes > 0):
        utility.printMessage("Retry for error: " + str(returnCode))

        # use the fallback data in input in case there is no result.
        if returnCode == ErrorCode.ACTION_RETRY_NO_RESULT:
          fillFallbackDataForAction(inputInfo, actionInfo)

        # else: no change on input and just retry for time out issues.
        returnCode = actionProcessor.processOneAction(actionInfo, inputInfo, inputInfo.has_key("DEBUG"))
        retryTimes = retryTimes - 1

      if returnCode != ErrorCode.ACTION_SUCCEED:
        # TODO: Prepare next_action handling logic, to allow condition and change of next action.
        utility.printError("ERROR when performing action: " + actionInfo["action_name"])
        utility.printError("      Subsequent actions are stopped.")
        break

      restoreFallbackDataForAction(inputInfo, backupData)
  
  return returnCode

# Return null if no substring.
# Doesn't support non-EN unicode yet.
def getSubstringForFallback(value):
  return " ".join(value.replace("-", " ").replace("_", " ").split(" ")[:-1])

def backupFallbackDataForAction(inputInfo, actionInfo):
  """
  Return an object with key/value pairs.
  """
  if 'retry_fallback' not in actionInfo:
    return {}

  backupData = {}
  for fallback in actionInfo['retry_fallback']:
    key = fallback['data_key']
    if not inputInfo.has_key(key):
      utility.printError(
          "No corresponding key in inputInfo to backup in the fallback data: " + key + ". Continued.",
          inputInfo)
    backupData[key] = inputInfo[key]
  
  return backupData

def restoreFallbackDataForAction(inputInfo, backupData):
  """
  Restore the values in backupData into inputInfo.
  """
  if not backupData:
    return

  for key in backupData:
    inputInfo[key] = backupData[key]

def fillFallbackDataForAction(inputInfo, actionInfo):
  if 'retry_fallback' not in actionInfo:
    return

  for fallback in actionInfo['retry_fallback']:
    key = fallback['data_key']
    if not inputInfo.has_key(key):
      utility.printError(
          "No corresponding key in inputInfo to fill in the fallback data: " + key + ". Continued.",
          inputInfo)
    old_value = inputInfo[key]

    fallback_type = fallback['fallback_type']
    fallback_value = ""
    if 'data_value' in fallback:
      fallback_value = fallback['data_value']
    if fallback_type == FallbackType.REPLACE_WITH_SUBSTRING:
      newValue = getSubstringForFallback(old_value)
      if newValue:
        fallback_value = newValue
    # else FallbackType.REPLACE_WITH_FIXED_VALUE

    inputInfo[key] = fallback_value
    utility.printMessage("Fallback the value " + key +
                         " from " + old_value + " to " + fallback_value)
      
def processOneOperationFromFile(productFileName):
  try:
    # Return False if failed, or True if done.
    productRequestFilePath = utility.getProductRequestFilePath(productFileName)
    (siteInfo, productInput) = request_info_loader.loadAddProductRequestFromFile(productRequestFilePath)
    utility.preFillInput(productInput)
    returnCode = processOneOperation(productInput, siteInfo, ADD_PRODUCT_OPERATIONS)

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


def loopProcessAddProductRequests():
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
      processOneOperationFromFile(fname)

    print "Sleep 2 seconds before continue. To stop press ctrl+c."
    time.sleep(2)

    # add product request file name should be like:
    # add_time_productname.txt
    # datetime.datetime.now().strftime("%Y%m%d%H%M%S")

if __name__ == "__main__":
  loopProcessAddProductRequests()

#productInput = utility.loadProductFromFile(
#    utility.getConfigureFilePath("test_product.txt"))
#processOneAction(ec21LoginAction, productInput, True)
#processOneAction(ec21SearchCategoryAction, productInput, True)
