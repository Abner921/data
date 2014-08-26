#coding=utf-8
from sms_v3_ReportService import *
import time
from datetime import datetime,date
from ApiSDKSoapClient import ApiSDKSoapClient
from ApiSDKSoapClient import printSoapResponse
from PreviewUtil import *
from urllib import urlopen
from Contants import Contants

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

if __name__ == "__main__":
    try:
        apiSDKSoapClient = ApiSDKSoapClient('sms','v3','ReportService','7034363')
        newClient = apiSDKSoapClient.newSoapClient()

        startDate = datetime(2014,5,7)
        endDate = datetime(2014,5,8)

        request = newClient.factory.create('getProfessionalReportIdRequest')
        reportRequestType = newClient.factory.create('getProfessionalReportIdRequest.reportRequestType')

        reportRequestType.performanceData= []
        reportRequestType.performanceData = ['cost','cpc','click','impression']
        reportRequestType.startDate = startDate
        reportRequestType.endDate = endDate
        reportRequestType.idOnly = False
        reportRequestType.levelOfDetails = 3
        reportRequestType.reportType = 10
        reportRequestType.format = 2
        reportRequestType.statRange = 2
        reportRequestType.unitOfTime = 7
        reportRequestType.device = 0

        request.reportRequestType = reportRequestType
        reportId=newClient.service.getProfessionalReportId(request.reportRequestType)

        res = newClient.last_received()
        reportId=res.getChild("Envelope").getChild("Body").getChild('getProfessionalReportIdResponse').getChild('reportId').getText()

        printSoapResponse(res)
        #-----------------------------------------------
        #get getReportState
        newClient.service.getReportState(reportId)
        res = newClient.last_received()
        isGenerated = res.getChild("Envelope").getChild("Body").getChild('getReportStateResponse').getChild('isGenerated').getText()

        if (isGenerated != '3'):
            for i in range(1, 5):
                time.sleep(10)
                newClient.service.getReportState(reportId)
                res = newClient.last_received()
                isGenerated = res.getChild("Envelope").getChild("Body").getChild('getReportStateResponse').getChild('isGenerated').getText()
                if isGenerated == '3':
                    break

        print "isGenerated:" + isGenerated
        #printSoapResponse(res)
        #-----------------------------------------------
        #getReportFileUrl
        if isGenerated == '3':
            newClient.service.getReportFileUrl(reportId)
            res = newClient.last_received()
            reportFileUrl= res.getChild("Envelope").getChild("Body").getChild('getReportFileUrlResponse').getChild('reportFilePath').getText()
            print "reportFileUrl:" + reportFileUrl
            #printSoapResponse(res)
            fileData=urlopen(reportFileUrl).read()
            f = file('/home/robin/demo_creative.csv',"wb")
            f.write(fileData)
            f.close()

    except Exception, e:
        print e
        tb.print_exc()




