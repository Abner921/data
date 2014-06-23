#!/usr/bin/env python

# -*- coding: unicode -*-
import sys,urllib,urllib2,gzip,StringIO,io,cookielib,re,socket,time,os,traceback,copy
from cookielib import CookieJar
from threading import Thread
import socket
from urllib2 import Request, urlopen, URLError, HTTPError
from Utility import Utility
from RequestInfoLoader import *
from SiteData import *
from ErrorCode import *

COOKIES_FILE = './kan_cookies.dat'
TIMEOUTS = 50

cj = None
opener = None
utility = Utility()
request_info_loader = RequestInfoLoader(utility)

socket.setdefaulttimeout(TIMEOUTS)

# Note: Don't install_opener as a global opener for now, considering
# timeouts. For each batch-send/fetch, we require one explicit login.
# Also, we don't use Basic Auth Handler.
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

def getEncodedUrl(actionInfo):
  if actionInfo.has_key("url_params") and actionInfo["url_params"]:
    return actionInfo["url"] + "?" + urllib.urlencode(actionInfo["url_params"])
  else:
    return actionInfo["url"]


def printActionRequestDebugInfo(shouldPrint, actionInfo, inputInfo, request):
  """ Only print, don't change the request / response
  """
  utility.printMessage("========================= Action: " + actionInfo["action_name"], shouldPrint)
  requestUrl = getEncodedUrl(actionInfo)
  payLoadData = getPayLoadData(actionInfo)
  utility.printMessage("========================= Request: " + requestUrl, shouldPrint)
  utility.printDebug(request, shouldPrint)
  utility.printDetails(payLoadData, shouldPrint)


def printActionResponseDebugInfo(shouldPrint, actionInfo, response, content):
  requestUrl = getEncodedUrl(actionInfo)
  utility.printMessage("========================= Response: " + requestUrl , shouldPrint)
  utility.printDebug(response, shouldPrint)
  utility.printMessage("========================= Response header", shouldPrint)
  utility.printDebug(response.headers, shouldPrint)
  utility.printMessage("", shouldPrint)
  utility.printMessage("========================= ResponseContent: " + requestUrl, shouldPrint)
  utility.printDetails(content, shouldPrint)
  utility.outputCookie(cj, "", shouldPrint)


def getPayLoadData(actionInfo):
  payLoadData = None
  if actionInfo.has_key("data") and actionInfo["data"]:
    if type(actionInfo["data"]) is str:
      payLoadData = actionInfo["data"]
    else:
      payLoadData = urllib.urlencode(actionInfo["data"])

  return payLoadData

def processActionError(actionInfo, content):
  if actionInfo.has_key("error_handling"):
    for errorInfo in actionInfo["error_handling"]:
      # print "error_regex: ", errorInfo["error_regex"]
      error_regex = getRegexMatcher(errorInfo, errorInfo["error_regex"])
      match_errors = error_regex.findall(content)
      if match_errors:
        if errorInfo.has_key("error_message"):
          error_message = errorInfo["error_message"]
        else:
          error_message = match_errors[0]

        if shouldRetry(errorInfo["error_code"]):
          error_message += "  Should retry."

        utility.printError(
            message = actionInfo["action_name"] + " error: " + error_message,
            isUserFacingError = True)
        return errorInfo["error_code"]

  return ErrorCode.ACTION_SUCCEED

def processActionResult(actionInfo, response, content, inputInfo, shouldPrint):
  if not actionInfo.has_key("result"):
    #utility.printError("No result regex defined.")
    return processActionError(actionInfo, content)

  resultActionInfos = actionInfo["result"]
  for resultActionInfo in resultActionInfos:
    matchResult = matchActionResult(resultActionInfo, response, content, shouldPrint)
    if matchResult is None:

      actionError = processActionError(actionInfo, content)
      if actionError != ErrorCode.ACTION_SUCCEED:
        return actionError
      else:
        # If no error matched, or no error handling, it still doesn't match expected result.
        utility.printError(
            message = actionInfo["action_name"] + " error: No result found.",
            isUserFacingError = True)
        return ErrorCode.ACTION_NO_RESULT

    else:
      if resultActionInfo.has_key("output_value"):
        inputInfo[resultActionInfo["output_key"]] = resultActionInfo["output_value"]
      else:
        inputInfo[resultActionInfo["output_key"]] = matchResult
      utility.printMessage(
          "SUCCEED: " + actionInfo["action_name"] + " Result: " + inputInfo[resultActionInfo["output_key"]])

  return ErrorCode.ACTION_SUCCEED

def getRegexMatcher(regMatchInfo, regPattern):
  """
  
  Note:
  re.S:.match any char including newline
  re.M:^$ match each line instead of the first line.
  >>> re.findall(r"^a(\d+)b", "a23b\na34b", re.M)
          ['23', '34']
  """
  caseSensitive = True
  matchMultiline = False
  if regMatchInfo.has_key("case_sensitive"):
    caseSensitive = regMatchInfo["case_sensitive"]
  if regMatchInfo.has_key("match_multiline"):
    matchMultiline = regMatchInfo["match_multiline"]
  regex_flag = 0
  if not caseSensitive:
    regex_flag = re.IGNORECASE
  if matchMultiline:
    regex_flag = regex_flag | re.S

  return re.compile(regPattern, regex_flag)

def matchActionResult(resultActionInfo, response, content, shouldPrint):
  checkRedirectUrl = resultActionInfo.has_key("response_regex")
  allMatches = None
  if checkRedirectUrl:
    # for the case when it is a 302 with redirect url when succeed
    redirect_regex = getRegexMatcher(resultActionInfo, resultActionInfo["response_regex"])
    responseStringIO = StringIO.StringIO()
    pprint(vars(response), responseStringIO)
    responseStringIO.write("\n")
    pprint(vars(response.headers), responseStringIO)
    responseObjectContent = responseStringIO.getvalue() + "\r\n" + utility.getCookieValues(cj)
    print "Response: ", responseObjectContent
    allMatches = redirect_regex.findall(responseObjectContent)
  else:
    result_regex = getRegexMatcher(resultActionInfo, resultActionInfo["result_regex"])
    allMatches = result_regex.findall(content)

  if len(allMatches) < 1:
    if checkRedirectUrl:
      utility.printError("Response has no matches for response regex: "
                         + resultActionInfo["response_regex"])
    else:
      utility.printError("Response has no matches for result regex: "
                         + resultActionInfo["result_regex"])
    #utility.printMessage(content, shouldPrint)
    return None
  else:
    if len(allMatches) > 1:
      utility.printMessage("Response has multiple matches for result. Getting the first one: " + allMatches[0])
      if checkRedirectUrl:
        utility.printMessage("Response Regex:" + resultActionInfo["response_regex"], shouldPrint)
      else:
        utility.printMessage("Result Regex:" + resultActionInfo["result_regex"])

    return allMatches[0]

def processOneAction(actionOriginInfo, inputInfo, shouldPrint):
  actionInfo = copy.deepcopy(actionOriginInfo)
  utility.processSiteData(actionInfo, inputInfo)

  utility.printMessage("Start: " + actionInfo["action_name"])
  if actionInfo.has_key("type") and actionInfo["type"] == "ADD_IMAGE":
    if not inputInfo.has_key("PRODUCT_IMAGE_FILE_PATH") or not inputInfo["PRODUCT_IMAGE_FILE_PATH"]:
      utility.printMessage("Skip image request as no image is uploaded")
      return ErrorCode.ACTION_SUCCEED

  requestUrl = getEncodedUrl(actionInfo)
  payLoadData = getPayLoadData(actionInfo)
  request = urllib2.Request(
      url = requestUrl,
      headers = actionInfo["headers"],
      data = payLoadData)
  printActionRequestDebugInfo(shouldPrint, actionInfo, inputInfo, request)

  try:
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') and response.info().get('Content-Encoding').find('gzip') >= 0:
      utility.printMessage('gzip enabled: suggest to remove the Content-Encoding setting!')
      buf = StringIO.StringIO(response.read())
      gzipFile = gzip.GzipFile(fileobj=buf)
      content = gzipFile.read()
    else:
      content = response.read()

    printActionResponseDebugInfo(shouldPrint, actionInfo, response, content)
    return processActionResult(actionInfo, response, content, inputInfo, shouldPrint)

  except HTTPError, e:
    utility.printError('The server couldn\'t fulfill the request. Error code: ' + str(e.code))
    if actionInfo.has_key('error_strategy'):
      if actionInfo['error_strategy'] == "ALLOW_ERROR":
        return ErrorCode.ACTION_SUCCEED
    return ErrorCode.ACTION_RETRY_HTTP_ERROR
  except URLError, e:
    utility.printError('We failed to reach a server. Reason: ' + str(e.reason))
    return ErrorCode.ACTION_RETRY_URL_ERROR
  except socket.timeout, e:
    errno, errstr = sys.exc_info()[:2]
    utility.printError("Socket Timeout (1): " + errno + ": " + errstr)
    return ErrorCode.ACTION_RETRY_TIMEOUT
  except socket.error, e:
    errno, errstr = sys.exc_info()[:2]
    if errno == socket.timeout:
      utility.printError("Socket Timeout (2): " + errno + ": " + errstr)
      return ErrorCode.ACTION_RETRY_TIMEOUT
    else:
      utility.printError("Socket Error: " + errno + ": " + errstr)
      return ErrorCode.ACTION_SOCKET_ERROR

def shouldRetry(returnCode):
  return (returnCode == ErrorCode.ACTION_RETRY_NO_RESULT or
          returnCode == ErrorCode.ACTION_RETRY_TIMEOUT or
          returnCode == ErrorCode.ACTION_RETRY_HTTP_ERROR or
          returnCode == ErrorCode.ACTION_RETRY_URL_ERROR)

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
      returnCode = processOneAction(actionInfo, inputInfo, inputInfo.has_key("DEBUG"))

      backupData = backupFallbackDataForAction(inputInfo, actionInfo)
      # Give it a couple retries for timeout or no-result-fallback.
      # Should only rety for timeout, or unknown reason, or explicitly retry request.
      # For login failure and other cases we should just fail fast.
      while (shouldRetry(returnCode) and retryTimes > 0):
        utility.printMessage("Retry for error: " + str(returnCode))

        # use the fallback data in input in case there is no result.
        if returnCode == ErrorCode.ACTION_RETRY_NO_RESULT:
          fillFallbackDataForAction(inputInfo, actionInfo)

        # else: no change on input and just retry for time out issues.
        returnCode = processOneAction(actionInfo, inputInfo, inputInfo.has_key("DEBUG"))
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
