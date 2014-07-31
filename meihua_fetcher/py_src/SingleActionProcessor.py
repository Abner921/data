#!/usr/bin/env python

# -*- coding: unicode -*-
import sys,urllib,urllib2,gzip,StringIO,io,cookielib,re,socket,time,os,traceback,copy
from cookielib import CookieJar
from threading import Thread
import socket
from urllib2 import Request, urlopen, URLError, HTTPError
from Utility import Utility
from SiteData import *
from ErrorCode import *
from pprint import pprint

TIMEOUTS = 50
socket.setdefaulttimeout(TIMEOUTS)
utility = Utility()

# Processor for one single action, for example, one post, one get, with one result check.
class SingleActionProcessor:

  cj = None

  # Initialize the cookie / opener.
  # It might NOT be thread safe, NOR can it support multiple action processor.
  def __init__(self):
    # Note: Don't install_opener as a global opener for now, considering
    # timeouts. For each batch-send/fetch, we require one explicit login.
    # Also, we don't use Basic Auth Handler.
    self.cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
    urllib2.install_opener(opener)

  def setCookie(self,cookieList):
    for cookie in cookieList:
      self.cj.set_cookie(cookie)
  
  def getCookieList(self):
    # get cookie array
    cookielist = []
    cookies = self.cj.__iter__()
    for cookie in cookies:
      cookielist.append(cookie) 
      
    return cookielist
  
  def getEncodedUrl(self, actionInfo):
    if actionInfo.has_key("url_params") and actionInfo["url_params"]:
      return actionInfo["url"] + "?" + urllib.urlencode(actionInfo["url_params"])
    else:
      return actionInfo["url"]


  def printActionRequestDebugInfo(self, shouldPrint, actionInfo, inputInfo, request):
    """ Only print, don't change the request / response
    """
    utility.printMessage("========= Action: " + actionInfo["action_name"], shouldPrint)
    utility.printMessage(actionInfo, shouldPrint)
    requestUrl = self.getEncodedUrl(actionInfo)
    payLoadData = self.getPayLoadData(actionInfo)
    utility.printMessage("========= Request: " + requestUrl, shouldPrint)
    utility.printDebug(request, shouldPrint)
    utility.printDetails(payLoadData, shouldPrint)
  
  
  def printActionResponseDebugInfo(self, shouldPrint, actionInfo, response, content):
    requestUrl = self.getEncodedUrl(actionInfo)
    utility.printMessage("========= Response: " + requestUrl , shouldPrint)
    utility.printDebug(response, shouldPrint)
    utility.printMessage("========= Response header", shouldPrint)
    utility.printDebug(response.headers, shouldPrint)
    utility.printMessage("", shouldPrint)
    utility.printMessage("========= Response Content: " + requestUrl, shouldPrint)
    utility.printDetails(content, shouldPrint)
    utility.printMessage("========= Response Cookie: " + requestUrl, shouldPrint)
    utility.outputCookie(self.cj, "", shouldPrint)
  
  
  def getPayLoadData(self, actionInfo):
    payLoadData = None
    if actionInfo.has_key("data") and actionInfo["data"]:
      if type(actionInfo["data"]) is str:
        payLoadData = actionInfo["data"]
      else:
        payLoadData = urllib.urlencode(actionInfo["data"])
  
    return payLoadData
  
  def processActionError(self, actionInfo, content):
    if actionInfo.has_key("error_handling"):
      for errorInfo in actionInfo["error_handling"]:
        # print "error_regex: ", errorInfo["error_regex"]
        error_regex = self.getRegexMatcher(errorInfo, errorInfo["error_regex"])
        match_errors = error_regex.findall(content)
        if match_errors:
          if errorInfo.has_key("error_message"):
            error_message = errorInfo["error_message"]
          else:
            error_message = match_errors[0]
  
          if self.shouldRetry(errorInfo["error_code"]):
            error_message += "  Should retry."
  
          utility.printError(
              message = actionInfo["action_name"] + " error: " + error_message,
              isUserFacingError = True)
          return errorInfo["error_code"]
  
    return ErrorCode.ACTION_SUCCEED
  
  # process the result, save the values into the inputInfo map with the result key specified in
  # action info, and then return the action code.
  # To get result: inputInfo[actionInfo["result"]["output_key"]]
  def processActionResult(self, actionInfo, response, content, inputInfo, shouldPrint):
    if not actionInfo.has_key("result"):
      #utility.printError("No result regex defined.")
      return self.processActionError(actionInfo, content)
  
    resultActionInfos = actionInfo["result"]
    for resultActionInfo in resultActionInfos:
      matchResult = self.matchActionResult(resultActionInfo, response, content, shouldPrint)
      if matchResult is None:
  
        actionError = self.processActionError(actionInfo, content)
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
            "========= SUCCEED: " + actionInfo["action_name"] + "\nResult: " + inputInfo[resultActionInfo["output_key"]])
  
    return ErrorCode.ACTION_SUCCEED
  
  def getRegexMatcher(self, regMatchInfo, regPattern):
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

  # right now this method only support one result (can't return a list)
  def matchActionResult(self, resultActionInfo, response, content, shouldPrint):
    checkRedirectUrl = resultActionInfo.has_key("response_regex")
    allMatches = None
    responseObjectContent = ""

    if checkRedirectUrl:
      # for the case when it is a 302 with redirect url when succeed
      redirect_regex = self.getRegexMatcher(resultActionInfo, resultActionInfo["response_regex"])
      responseStringIO = StringIO.StringIO()
      pprint(vars(response), responseStringIO)
      responseStringIO.write("\n")
      pprint(vars(response.headers), responseStringIO)
      responseObjectContent = responseStringIO.getvalue() + "\r\n" + utility.getCookieValues(self.cj)
      allMatches = redirect_regex.findall(responseObjectContent)
    else:
      result_regex = self.getRegexMatcher(resultActionInfo, resultActionInfo["result_regex"])
      allMatches = result_regex.findall(content)
  
    if len(allMatches) < 1:
      if checkRedirectUrl:
        utility.printError("Response has no matches for response regex: "
                           + resultActionInfo["response_regex"] + " Content: " + responseObjectContent)
      else:
        utility.printError("Response has no matches for result regex: "
                           + resultActionInfo["result_regex"] + " Content: " +  content)
      return None
    else:
      if len(allMatches) > 1:
        utility.printMessage("Response has multiple matches for result. Getting the first one: " + allMatches[0], shouldPrint)
        if checkRedirectUrl:
          utility.printMessage("Response Regex:" + resultActionInfo["response_regex"], shouldPrint)
        else:
          utility.printMessage("Result Regex:" + resultActionInfo["result_regex"], shouldPrint)
  
      return allMatches[0]
  
  def processOneAction(self, inputInfo, actionOriginInfo, shouldPrint):
    actionInfo = copy.deepcopy(actionOriginInfo)
    utility.processSiteData(actionInfo, inputInfo)

    utility.printMessage("========= Start: " + actionInfo["action_name"])
    if actionInfo.has_key("type") and actionInfo["type"] == "ADD_IMAGE":
      if not inputInfo.has_key("PRODUCT_IMAGE_FILE_PATH") or not inputInfo["PRODUCT_IMAGE_FILE_PATH"]:
        utility.printMessage("Skip image request as no image is uploaded")
        return ErrorCode.ACTION_SUCCEED
  
    requestUrl = self.getEncodedUrl(actionInfo)
    payLoadData = self.getPayLoadData(actionInfo)
    request = urllib2.Request(
        url = requestUrl,
        headers = actionInfo["headers"],
        data = payLoadData)
    self.printActionRequestDebugInfo(shouldPrint, actionInfo, inputInfo, request)
  
    try:
      response = urllib2.urlopen(request)
      if response.info().get('Content-Encoding') and response.info().get('Content-Encoding').find('gzip') >= 0:
        utility.printMessage('gzip enabled: suggest to remove the Content-Encoding setting!', shouldPrint)
        buf = StringIO.StringIO(response.read())
        gzipFile = gzip.GzipFile(fileobj=buf)
        content = gzipFile.read()
      else:
        content = response.read()
  
      self.printActionResponseDebugInfo(shouldPrint, actionInfo, response, content)
      return self.processActionResult(actionInfo, response, content, inputInfo, shouldPrint)
  
    except HTTPError, e:
      utility.printError(str(e))
      utility.printError('The server couldn\'t fulfill the request. Error code: ' + str(e.code))
      if actionInfo.has_key('error_strategy'):
        if actionInfo['error_strategy'] == "ALLOW_ERROR":
          return ErrorCode.ACTION_SUCCEED
      return ErrorCode.ACTION_RETRY_HTTP_ERROR
    except URLError, e:
      utility.printError(str(e))
      utility.printError('We failed to reach a server. Reason: ' + str(e.reason))
      return ErrorCode.ACTION_RETRY_URL_ERROR
    except socket.timeout, e:
      utility.printError(str(e))
      errno, errstr = sys.exc_info()[:2]
      utility.printError("Socket Timeout (1): " + str(errno) + ": " + str(errstr))
      return ErrorCode.ACTION_RETRY_TIMEOUT
    except socket.error, e:
      utility.printError(str(e))
      errno, errstr = sys.exc_info()[:2]
      if errno == socket.timeout:
        utility.printError("Socket Timeout (2): " + str(errno) + ": " + str(errstr))
        return ErrorCode.ACTION_RETRY_TIMEOUT
      else:
        utility.printError("Socket Error: " + str(errno) + ": " + str(errstr))
        return ErrorCode.ACTION_SOCKET_ERROR
  
  def shouldRetry(self, returnCode):
    return (returnCode == ErrorCode.ACTION_RETRY_NO_RESULT or
            returnCode == ErrorCode.ACTION_RETRY_TIMEOUT or
            returnCode == ErrorCode.ACTION_RETRY_HTTP_ERROR or
            returnCode == ErrorCode.ACTION_RETRY_URL_ERROR)

  
  """
  Process one action with limited retry times depending on the retry / fallback logic.
  The inputInfo will be changed for output purpose.
  """
  def processOneActionWithRetry(self, inputInfo, actionInfo, retryTimes = 3):
    returnCode = self.processOneAction(inputInfo, actionInfo, inputInfo.has_key("DEBUG"))
    backupData = self.backupFallbackDataForAction(inputInfo, actionInfo)
    # Give it a couple retries for timeout or no-result-fallback.
    # Should only rety for timeout, or unknown reason, or explicitly retry request.
    # For login failure and other cases we should just fail fast.
    while (self.shouldRetry(returnCode) and retryTimes > 0):
      utility.printMessage("Retry for error: " + str(returnCode))
  
      # use the fallback data in input in case there is no result.
      if returnCode == ErrorCode.ACTION_RETRY_NO_RESULT:
        self.fillFallbackDataForAction(inputInfo, actionInfo)
  
      # else: no change on input and just retry for time out issues.
      returnCode = self.processOneAction(inputInfo, actionInfo, inputInfo.has_key("DEBUG"))
      retryTimes = retryTimes - 1
  
    if returnCode != ErrorCode.ACTION_SUCCEED:
      # TODO: Prepare next_action handling logic, to allow condition and change of next action.
      utility.printError("ERROR when performing action: " + actionInfo["action_name"])
      utility.printError("      Subsequent actions are stopped.")
  
    self.restoreFallbackDataForAction(inputInfo, backupData)
    return returnCode


  """
  Return an object with key/value pairs.
  """
  def backupFallbackDataForAction(self, inputInfo, actionInfo):
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
  
  """
  Restore the values in backupData into inputInfo.
  """
  def restoreFallbackDataForAction(self, inputInfo, backupData):
    if not backupData:
      return
  
    for key in backupData:
      inputInfo[key] = backupData[key]
  
    
  # Return null if no substring.
  # Doesn't support non-EN unicode yet.
  def getSubstringForFallback(self, value):
    return " ".join(value.replace("-", " ").replace("_", " ").split(" ")[:-1])
  

  def fillFallbackDataForAction(self, inputInfo, actionInfo):
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
        newValue = self.getSubstringForFallback(old_value)
        if newValue:
          fallback_value = newValue
      # else FallbackType.REPLACE_WITH_FIXED_VALUE
  
      inputInfo[key] = fallback_value
      utility.printMessage("Fallback the value " + key +
                           " from " + old_value + " to " + fallback_value)
