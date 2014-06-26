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
# Note: Don't install_opener as a global opener for now, considering
# timeouts. For each batch-send/fetch, we require one explicit login.
# Also, we don't use Basic Auth Handler.
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
utility = Utility()

# Processor for one single action, for example, one post, one get, with one result check.
class SingleActionProcessor:

  def getEncodedUrl(self, actionInfo):
    if actionInfo.has_key("url_params") and actionInfo["url_params"]:
      return actionInfo["url"] + "?" + urllib.urlencode(actionInfo["url_params"])
    else:
      return actionInfo["url"]
  

  def printActionRequestDebugInfo(self, shouldPrint, actionInfo, inputInfo, request):
    """ Only print, don't change the request / response
    """
    utility.printMessage("========================= Action: " + actionInfo["action_name"], shouldPrint)
    requestUrl = self.getEncodedUrl(actionInfo)
    payLoadData = self.getPayLoadData(actionInfo)
    utility.printMessage("========================= Request: " + requestUrl, shouldPrint)
    utility.printDebug(request, shouldPrint)
    utility.printDetails(payLoadData, shouldPrint)
  
  
  def printActionResponseDebugInfo(self, shouldPrint, actionInfo, response, content):
    requestUrl = self.getEncodedUrl(actionInfo)
    utility.printMessage("========================= Response: " + requestUrl , shouldPrint)
    utility.printDebug(response, shouldPrint)
    utility.printMessage("========================= Response header", shouldPrint)
    utility.printDebug(response.headers, shouldPrint)
    utility.printMessage("", shouldPrint)
    utility.printMessage("========================= ResponseContent: " + requestUrl, shouldPrint)
    utility.printDetails(content, shouldPrint)
    utility.outputCookie(cj, "", shouldPrint)
  
  
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
            "SUCCEED: " + actionInfo["action_name"] + " Result: " + inputInfo[resultActionInfo["output_key"]])
  
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
    if checkRedirectUrl:
      # for the case when it is a 302 with redirect url when succeed
      redirect_regex = self.getRegexMatcher(resultActionInfo, resultActionInfo["response_regex"])
      responseStringIO = StringIO.StringIO()
      pprint(vars(response), responseStringIO)
      responseStringIO.write("\n")
      pprint(vars(response.headers), responseStringIO)
      responseObjectContent = responseStringIO.getvalue() + "\r\n" + utility.getCookieValues(cj)
      print "Response: ", responseObjectContent
      allMatches = redirect_regex.findall(responseObjectContent)
    else:
      result_regex = self.getRegexMatcher(resultActionInfo, resultActionInfo["result_regex"])
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
  
  def processOneAction(self, actionOriginInfo, inputInfo, shouldPrint):
    actionInfo = copy.deepcopy(actionOriginInfo)
    utility.processSiteData(actionInfo, inputInfo)
  
    utility.printMessage("Start: " + actionInfo["action_name"])
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
        utility.printMessage('gzip enabled: suggest to remove the Content-Encoding setting!')
        buf = StringIO.StringIO(response.read())
        gzipFile = gzip.GzipFile(fileobj=buf)
        content = gzipFile.read()
      else:
        content = response.read()
  
      self.printActionResponseDebugInfo(shouldPrint, actionInfo, response, content)
      return self.processActionResult(actionInfo, response, content, inputInfo, shouldPrint)
  
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
  
  def shouldRetry(self, returnCode):
    return (returnCode == ErrorCode.ACTION_RETRY_NO_RESULT or
            returnCode == ErrorCode.ACTION_RETRY_TIMEOUT or
            returnCode == ErrorCode.ACTION_RETRY_HTTP_ERROR or
            returnCode == ErrorCode.ACTION_RETRY_URL_ERROR)