import sys,urllib,urllib2,gzip,StringIO,io,cookielib,re,socket,time,os,traceback,copy
from cookielib import CookieJar
from threading import Thread
import socket
from urllib2 import Request, urlopen, URLError, HTTPError

cj = None
opener = None

TIMEOUTS = 50
socket.setdefaulttimeout(TIMEOUTS)

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
request = None
response = None
content = ""

def doRequest(actionInfo):
  # getPayLoadData(actionInfo):
  payLoadData = None
  if actionInfo.has_key("data") and actionInfo["data"]:
    if type(actionInfo["data"]) is str:
      payLoadData = actionInfo["data"]
    else:
      payLoadData = urllib.urlencode(actionInfo["data"])
  
  request = urllib2.Request(
      url = actionInfo["url"],
      headers = actionInfo["headers"],
      data = payLoadData)
  
  response = urllib2.urlopen(request)
  return response
  

def requestUrl(urlRequest):
  request = urllib2.Request(urlRequest)
  return urllib2.urlopen(request)

def printCookie():
  print ("========= COOKIE: ")
  for index, cookie in enumerate(cj):
    print (str(index) + '  :  ' + str(cookie))

def getResponse(response):
  if response.info().get('Content-Encoding') and response.info().get('Content-Encoding').find('gzip') >= 0:
    print ('gzip enabled!')
    buf = StringIO.StringIO(response.read())
    gzipFile = gzip.GzipFile(fileobj=buf)
    content = gzipFile.read()
  else:
    content = response.read()
  
  return content

def findReg(content, reg):
  result_regex = re.compile(reg)
  allMatches = result_regex.findall(content)
  print "All matches: "
  for match in allMatches:
    print match
  return allMatches

def find(content, actionInfo):
  return findReg(content, actionInfo["result_regex"])

print ".... Use actionInfo, response, request, printCookie, doRequest, getResponse ..."


actionInfo = {
  'action_name': 'view product list on manufacturer after login',
  'headers': { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               #'Accept-Encoding': 'gzip,deflate,sdch',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'my.manufacturer.com',
               'Referer': 'http://my.manufacturer.com/jpc/signin.a?url=http%3A%2F%2Fwww.manufacturer.com%2Fbusiness%2Fmy%2Faccount.a%3Faction%3DView'},
  'result': [ { 'output_key': 'manufacturer_ID',
                'result_regex': '(.*)'}],
  'url': 'http://www.manufacturer.com/business/my/account.a?action=View'
}
response = doRequest(actionInfo)
printCookie()
content = getResponse(response)
#response = requestUrl("http://www.manufacturer.com/business/my/account.a?action=View")
print content.find("Sign Out")



# test regex:

import re
content = """
  cat1=new Category(root, "31","Automobile")
    cat2=new Category(cat1, "746","ATV")
    cat2=new Category(cat1, "322","Auto Accessories")
    cat2=new Category(cat1, "1184","Auto Electrical System")
      cat3=new Category(cat2, "1182","Auto Batteries")
      cat3=new Category(cat2, "1186","Auto Ignition System")
"""
def match(pattern):
  reg = re.compile(pattern, re.IGNORECASE)
  allMatches = reg.findall(content)
  print "All matches: "
  for match in allMatches:
    print match
  return allMatches

"new Category\(.*,.*\"/(d+)\".*,.*auto.*\)"
