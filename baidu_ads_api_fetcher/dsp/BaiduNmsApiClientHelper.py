import suds
import sys
import ConfigParser
import traceback as tb

'''
    webservice client
'''
class BaiduNmsApiClient():
    def __init__(self, service): 
        try:
            self.initConfig()
            url = self.serverUrl + '/sem/nms/v2/' + service + '?wsdl'
            client = suds.client.Client(url)
            print client    #The soap client stub
            header = client.factory.create('ns0:AuthHeader')
            header.username = self.username
            header.password = self.password
            header.token = self.token
            header.target = self.target
            client.set_options(soapheaders=header)
            print header    #The soap AuthHeader
            self.client = client
        except Exception, e:
            print e
            tb.print_exc()
            
    def initConfig(self):
        cf = ConfigParser.ConfigParser()
        cf.read("baidu-api.properties")
        self.serverUrl=cf.get("nms", "serverUrl")
        self.username=cf.get("nms", "username")
        self.password=cf.get("nms", "password")
        self.token=cf.get("nms", "token")
        self.target=cf.get("nms", "target")
        self.client=None

'''
    print response result
'''
def printSoapResponse(res):
        resheader = res.getChild("Envelope").getChild("Header").getChild("ResHeader")
        resbody = res.getChild("Envelope").getChild("Body")
        failures = resheader.getChild("failures")
        print "Response Header=>"
        print "Execution result: \t", resheader.getChild("desc").getText()
        print "      operations: \t", resheader.getChild("oprs").getText()
        print "  operation time: \t", resheader.getChild("oprtime").getText()
        print "   consume quota: \t", resheader.getChild("quota").getText()
        print "    remain quota: \t", resheader.getChild("rquota").getText()
        print "          status: \t", resheader.getChild("status").getText()
        if failures is not None:
            print "            code: \t", failures.getChild("code").getText()
            print "         message: \t", failures.getChild("message").getText()
            print "        position: \t", failures.getChild("position").getText();
        print "Response Body=>"
        if resbody is not None:
            print resbody



