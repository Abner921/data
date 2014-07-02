#!/usr/bin/env python

from pprint import pprint
import os, re, sys, datetime, StringIO, time, calendar

class Utility:
  """Utils to load file / print debug
  """

  logStream = StringIO.StringIO()
  requestLogStream = StringIO.StringIO()
  detailLogStream = StringIO.StringIO()
  # the stream for final user facing error message file.
  errorContentStream = StringIO.StringIO()
  
  def saveLogFile(self, productFileName):
    # filename contains full path
    print " =======  saveLogFile", productFileName
    log_file = open(self.getLogFileName(productFileName), "w+")
    log_file.write(self.logStream.getvalue())
    log_file.close()
    # reset to a new stream once done.
    self.logStream = StringIO.StringIO()

    log_file = open(self.getRequestLogFileName(productFileName), "w+")
    log_file.write(self.requestLogStream.getvalue())
    log_file.close()
    # reset to a new stream once done.
    self.requestLogStream = StringIO.StringIO()

    detail_file = open(self.getDetailLogFileName(productFileName), "w+")
    detail_file.write(self.detailLogStream.getvalue())
    detail_file.close()
    # reset to a new stream once done.
    self.detailLogStream = StringIO.StringIO()

    error_file = open(self.getErrorMessageFileName(productFileName), "w+")
    error_file.write(self.errorContentStream.getvalue())
    error_file.close()
    # reset to a new stream once done.
    self.errorContentStream = StringIO.StringIO()
    

  def getLogFileName(self, productFileName):
    return productFileName[: -4] + "_log.txt"

  def getRequestLogFileName(self, productFileName):
    return productFileName[: -4] + "_log_request.txt"

  def getDetailLogFileName(self, productFileName):
    return productFileName[: -4] + "_log_detail.txt"

  # the file for storing the user facing error message
  def getErrorMessageFileName(self, productFileName):
    return productFileName[: -4] + "_error.txt"

  def printMessage(self, message, printToStdout = True):
    self.printDebug(message, printToStdout)

  def printDetails(self, details, printToStdout = True):
    if printToStdout:
      print details

    self.detailLogStream.write(details)
    self.detailLogStream.write("\r\n")
    self.detailLogStream.write("----------------------------\r\n")
    self.detailLogStream.write("============================\r\n")
    self.detailLogStream.write("----------------------------\r\n")
    self.detailLogStream.write("\r\n")

  def printDebug(self, obj, printToStdout = True):
    # or, use pprint(dir(obj))

    if hasattr(obj, "__dict__"):
      if printToStdout:
        pprint(vars(obj))
        pprint(vars(obj), self.logStream)

      pprint(vars(obj), self.requestLogStream)
    else:
      if printToStdout:
        print obj
        self.logStream.write(obj)
        self.logStream.write("\r\n")

      self.requestLogStream.write(obj)
      self.requestLogStream.write("\r\n")


  def printError(self, message, obj = "", isUserFacingError = True):
    errorMsg = "===== ERROR ===== " + message

    print errorMsg
    self.logStream.write(errorMsg)
    self.logStream.write("\r\n")

    self.requestLogStream.write(errorMsg)
    self.requestLogStream.write("\r\n")

    if isUserFacingError:
      self.errorContentStream.write(message)
      self.errorContentStream.write("\r\n")

    if obj:
      self.printDebug(obj, True)

  def getCookieValues(self,  cj):
    cookieString = ""
    for index, cookie in enumerate(cj):
      cookieString += str(cookie) + "\r\n"
    return cookieString

  def outputCookie(self,  cj, cookieFile, printToStdout = True):
    self.printMessage("========= COOKIE: ", printToStdout)
    self.printMessage(self.getCookieValues(cj), printToStdout)

    if (cookieFile):
      cj.save(cookieFile)

  def getStartingPath(self):
    # Gets the starting path from where this application is called.
    return os.getcwd()

  def getApplicationPath(self):
    # Gets the Path where SendRequest.py is:
    return sys.path[0]    #sys.argv[0]

  def getThisFilePath(self):
    # Gets the path of this Utility.py
    return os.path.split(os.path.realpath(__file__))[0]

  def convertCamelCaseToUnderScore(self, content):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', content)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
