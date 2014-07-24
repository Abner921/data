#!/usr/bin/env python

from pprint import pprint
import os, re, sys, datetime, StringIO, time, calendar


def enum(**enums):
    return type('Enum', (), enums)


class Utility:
  """Utils to load file / print debug
  """

  __STRING_KEY_BEGIN__ = '%==>'
  __STRING_KEY_END__ = '<==%'
  __OBJECT_KEY_BEGIN__ = '%-->'
  __OBJECT_KEY_END__ = '<--%'

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


  def printError(self, message, obj = "", isUserFacingError = False):
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

  def preFillInput(self, input):
    """Fill some predefined consts which can be used for the requests.
    
    Note: as the prefilled data might change over time, it should be only
    called once per-product-operation.
    
    All available marcos can be found in all_field_marco.txt
    """
    input["CURRENT_DATE_LENGTH_8"] = datetime.datetime.now().strftime("%Y%m%d")
    input["CURRENT_TIME_LENGTH_6"] = datetime.datetime.now().strftime("%H%M%S")
    input["CURRENT_MILLI_LENGTH_3"] = datetime.datetime.now().strftime("%f")[3:]
    input["CURRENT_MILLI_LENGTH_6"] = datetime.datetime.now().strftime("%f")
    long_time_random = (str(calendar.timegm(datetime.datetime.now().timetuple()))
                        + datetime.datetime.now().strftime("%f"))
    input["RANDOM_13"] = long_time_random[:13]
    time.sleep(0.1)
    long_time_random = (str(calendar.timegm(datetime.datetime.now().timetuple()))
                        + datetime.datetime.now().strftime("%f"))
    input["RANDOM_13_OTHER"] = long_time_random[:13]
    #sprint "http://upimage.ec21.com/upload/temporary/PI_jymeilun2012_" + input["CURRENT_DATE_LENGTH_8"] + input["CURRENT_TIME_LENGTH_6"] + input["CURRENT_MILLI_LENGTH_3"] + "_3.jpg"



  def processSiteData(self, data, input):
    """ Process and replace all macros in the data, recursively.
    input = {
       'STRING_KEY' : '...',
       'OBJECT_KEY' : {...}
    }
    data = {
      'key1' : 'value %==>STRING_KEY<==%',
      ...
      'key2' : '%-->OBJECT_KEY<--%',
    }
    """
    if not type(data) is dict:
      return

    for k in data:
      if type(data[k]) is dict:
        self.processSiteData(data[k], input)

      if type(data[k]) is list:
        for item in data[k]:
          self.processSiteData(item, input)

      if type(data[k]) is str:
        # loop util all macros are replaced.
        while True:
          macro_key, is_string = self.getMacroKey(data[k])
          if not macro_key:
            break;
          data[k] = self.replaceMacro(input, data[k], macro_key, is_string)
          if not type(data[k]) is str:
            # replace the macro inside the object.
            self.processSiteData(data[k], input)
            break

  def getMacroKey(self, value):
    """ Returns <key_name, is_string>
    """
    if (value.startswith(self.__OBJECT_KEY_BEGIN__)
        and value.endswith(self.__OBJECT_KEY_END__)):
      return (value[len(self.__OBJECT_KEY_BEGIN__)
              : len(value) - len(self.__OBJECT_KEY_END__)]), False

    begin_index = value.find(self.__STRING_KEY_BEGIN__)
    end_index = value.find(self.__STRING_KEY_END__)
    if (begin_index >= 0 and end_index > begin_index):
      return (value[begin_index + len(self.__STRING_KEY_BEGIN__)
              : end_index]), True

    return "", False

  def replaceMacro(self, input, value, key, is_string):
    if input.has_key(key):
      input_value = input[key]
    else:
      self.printError("Input has no value for key: " + key, input)
      input_value = ""

    if is_string:
      macro_key = self.__STRING_KEY_BEGIN__ + key + self.__STRING_KEY_END__
      # print "---------- value: ", value, " macro: ", macro_key, " input_value: ", input_value 
      return value.replace(macro_key, str(input_value))
    else:
      return input_value

  """
  Utils for getting the file path:
      print "current cwd: ", os.getcwd()
      print "reapath: ", os.path.split(os.path.realpath(__file__))[0]
      print "filepath: ", sys.path[0], ", ", sys.argv[0]
  """

  def getStartingPath(self):
    # Gets the starting path from where this application is called.
    return os.getcwd()

  def getApplicationPath(self):
    # Gets the Path where SendRequest.py is:
    return sys.path[0]    #sys.argv[0]

  def getThisFilePath(self):
    # Gets the path of this Utility.py
    return os.path.split(os.path.realpath(__file__))[0]

  def markProductRequestAsFailed(self, fileName):
    if os.path.isfile(self.getProductErrorFilePath(fileName)):
      os.remove(self.getProductErrorFilePath(fileName))

    os.rename(self.getProductRequestFilePath(fileName),
              self.getProductErrorFilePath(fileName))
    self.saveLogFile(self.getProductErrorFilePath(fileName))

  def markProductRequestAsFinished(self, fileName):
    if os.path.isfile(self.getProductFinishFilePath(fileName)):
      os.remove(self.getProductFinishFilePath(fileName))

    os.rename(self.getProductRequestFilePath(fileName),
              self.getProductFinishFilePath(fileName))
    self.saveLogFile(self.getProductFinishFilePath(fileName))

  def getProductRequestPath(self):
    # All the requests in progress or not started.
    return os.path.join(self.getApplicationPath(), "../products/requested")

  def getProductRequestFilePath(self, fileName):
    return os.path.join(self.getProductRequestPath(), fileName)
  
  def getProductErrorPath(self):
    # Folder with error logs
    return os.path.join(self.getApplicationPath(), "../products/failed")

  def getProductErrorFilePath(self, fileName):
    return os.path.join(self.getProductErrorPath(), fileName)

  def getProductFinishPath(self):
    # This folder should be clear-up regularly.
    return os.path.join(self.getApplicationPath(), "../products/finished")

  def getProductFinishFilePath(self, fileName):
    return os.path.join(self.getProductFinishPath(), fileName)

  def listProductRequestFiles(self, path):
    dirList=os.listdir(path)
    for fname in dirList:
      self.printMessage(fname)

  def convertCamelCaseToUnderScore(self, content):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', content)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

"""
  def xpath(self, html):
    from lxml import etree
    from xml.dom import minidom
    if html == None:
        print "Empty HTML "
        continue
    
    try:
        subtree = etree.HTML(html)
        subnodes = subtree.xpath("//td[@class=frame_style_padding]")
    except:
        self.printDebug(html, false)

import xpath
 import xml.dom.minidom
 xml = xml.dom.minidom.parse('/tmp/books.xml')
 doc = xml.documentElement
 xpath.find('/bookstore/book[1]', doc)[0].toxml()
 xpath.find('/bookstore', doc)

 
    def operate(node,cmd,para = None):
        try:
            if cmd == "..":
                return node.parentNode
            elif cmd == ".":
                return node
            elif cmd == "/":
                return node
            elif cmd == "//":
                pass
            elif cmd == "@":
                for i in range(len(node.attributes.items())):
                    nodeattr = node.attributes.item(i)
                    print(nodeattr)
                    if nodeattr.nodeName == para:
                        return nodeattr
            elif cmd == "=":
                if node.nodeValue == para:
                    return node
            else:
                for node_tag in node.childNodes:
                    if node_tag.nodeName == cmd:
                        return node_tag
        except (DOMException,IndexError) as Err:
            print("got Exception".format(Err))
   
    cmdlist = interpeter(XPath_Str)
    node = Node
    para = None
   
    while len(cmdlist)>0:
        cmd = cmdlist.pop(0)
        if cmd in keyword2:
            para = cmdlist.pop(0)
        node = operate(node,cmd,para)
    return node
    
    
  def loadCookie(self, cookieFile):
    FileCookieJar.load(cookieFile)

  def startThread(self, myfunc):
    t = Thread(target=myfunc, args=(i,))
    t.start()

  def testParseResponse(self):
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        self.printMessage('gzip enabled')
        buf = StringIO.StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    self.printMessage("Success-----------------\n" + data)

  def testAddCookie(self):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'cookiename=cookievalue'))
    f = opener.open("http://example.com/")

  def testLoginSinaMail(self):   
    # for mail.sina.com.cn

    cj = cookielib.CookieJar()  
    url_login = 'http://mail.sina.com.cn/cgi-bin/login.cgi'  
    body = (('logintype','login'), ('u','username'),  
    ('psw', '********'))
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))  
    #opener.addheaders = [('User-agent', 'Opera/9.23')]  
    opener.addheaders = [('User-agent',  
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
    urllib2.install_opener(opener)  
    req=urllib2.Request(url_login,urllib.urlencode(body))  
    u=urllib2.urlopen(req)
    print u.read().decode('utf-8').encode('gbk')

  def testCookieJar(self):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # input-type values from the html form
    values = { "username" : username, "password": password, "login" : "Login" , "PK_AccessPoint" : "0" }
    data = urllib.urlencode(values)
    response = opener.open("https://page.com/login.php", data)
    content = response.read()


  def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

  def encode_multipart_formdata(fields, files):
    LIMIT = '----------lImIt_of_THE_fIle_eW_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + LIMIT)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + LIMIT)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + LIMIT + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

  def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

"""

