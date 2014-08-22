import suds
import datetime
import time
import sys
import os
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse
from urllib import urlopen
from ReportParser import ReportParser
from MongoUtil import save_report

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

if __name__ == "__main__":
    try:
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('ReportService')
        client = baiduApiSoap.client

		#==== get report id ====
        # contruct request body
        request = client.factory.create('getReportIdRequest')
        reportType = client.factory.create('getReportIdRequest.reportRequestType')
        reportType.performanceData = ['srch','click','cost','ctr','cpm','acp']
        reportType.startDate = datetime.datetime(int(2014),int(8),int(7))
        reportType.endDate = datetime.datetime(int(2014),int(8),int(20))
        reportType.idOnly = False
        reportType.format = 1 #csv
        reportType.reportType = 2
        #request.statRange = 2
        #request.statIds = [757446,757447,757448]
        request.reportRequestType = reportType

        # send request
        reportId = client.service.getReportId(request.reportRequestType)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)

        #==== get report status ====
        # contruct request body
        request = client.factory.create('getReportStateRequest')
        request.reportId = reportId
        status = None
        retry = 1
        while(status != 3): # 3 means report generated successfully
            if retry > 3:
                break
            print 'sleep 10 seconds to wait report generated...'
            time.sleep(2)
            print request
            status = client.service.getReportState(request.reportId)
            print 'status=' + str(status)
            retry += 1
        if status != 3:
            print 'report generated with failure so exit'
            sys.exit(1)
        else:
            print 'report generated successfully!'

        #==== get report file url ====
        # contruct request body
        request = client.factory.create('getReportFileUrlRequest')
        request.reportId = reportId
        fileUrl = client.service.getReportFileUrl(request.reportId)
        print 'fileUrl=' + fileUrl

        #get file
        fileDirPath = '/home/robin/'
        fileName = 'wangmeng.csv'
        filePath = os.path.join(fileDirPath,fileName)
        fileData=urlopen(fileUrl).read()
        f = file(filePath,"wb")
        f.write(fileData)
        f.close()
        print "save data into file:"+filePath

        parseReport = ReportParser(filePath)

        for rowDict in parseReport.parseCsvFileBody():
            save_report(rowDict)

    except Exception, e:
        print e
        tb.print_exc()

