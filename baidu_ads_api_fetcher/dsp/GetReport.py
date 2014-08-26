#encoding=utf-8
import suds
import time
import sys
import os
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse
from urllib import urlopen
from ReportParser import ReportParser
from MongoUtil import save_report
from LoggingUtil import getLogger
from datetime import datetime,date,timedelta

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# TODO (robin): contition filter
# TODO (robin): add realtime report
# TODO (robin): design function and params

log = getLogger()

class Report():

    def __init__(self):
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('ReportService')
        client = baiduApiSoap.client

        self.client = client
        self.requestParams={}
        self.request = None
        self.reportTypeDesc = None
        self.__init_requestParams()

    def __init_requestParams(self):

        self.requestParams['performanceData']= ['srch','click','cost','ctr','cpm','acp']
        #self.requestParams['startDate'] = startDate
        #self.requestParams['endDate'] = endDate
        self.requestParams['idOnly'] = False
        #self.requestParams['levelOfDetails'] = 7
        #self.requestParams['reportType'] = 2
        self.requestParams['format'] = 1 #csv
        self.requestParams['statRange'] = 2

    def setRequestParamStatRange(self,statRange):
        self.requestParams['statRange'] = statRange
    def setRequestParamIdOnly(self,idOnly):
        self.requestParams['idOnly'] = idOnly

    def __genRequest(self):
        request = self.client.factory.create('getReportIdRequest')
        reportRequestType = self.client.factory.create('getReportIdRequest.reportRequestType')

        reportRequestType.performanceData = self.requestParams['performanceData']
        reportRequestType.startDate       = self.requestParams['startDate']
        reportRequestType.endDate         = self.requestParams['endDate']
        reportRequestType.idOnly          = self.requestParams['idOnly'] #
        reportRequestType.reportType      = self.requestParams['reportType']
        reportRequestType.format          = self.requestParams['format']  # 1:csv
        reportRequestType.statRange       = self.requestParams['statRange']   #统计粒度  2：账户范围 3：推广组 4 :创意

        request.reportRequestType = reportRequestType
        self.request = request

    def genCampaignRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Campaign'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['reportType'] = 2

        self.__genRequest()

    def genAdgroupRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Adgroup'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['reportType'] = 3

        self.__genRequest()

    def genKeywordRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Keyword'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['reportType'] = 5

        self.__genRequest()

    def genCreativeRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Creative'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['reportType'] = 4

        self.__genRequest()

    def genWordRequest(self,startDate,endDate):
        self.reportTypeDesc = 'Word'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['reportType'] = 6

        self.__genRequest()

    def genRegionRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Region'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['reportType'] = 11

        self.__genRequest()

    def genSiteRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Site'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['reportType'] = 7

        self.__genRequest()

    def genIndustryRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Industry'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['reportType'] = 15

        self.__genRequest()


    #----------------------------------
    def __getReportId(self):
        reportId=self.client.service.getReportId(self.request.reportRequestType)
        res = self.client.last_received()
        self.reportId = reportId
        #printSoapResponse(res)
        log.info("reportId:" + reportId)

    def __getReportState(self):
        isGenerated = self.client.service.getReportState(self.reportId)
        res = self.client.last_received()

        if (isGenerated != 3):
            for i in range(1, 5):
                time.sleep(10)
                isGenerated = self.client.service.getReportState(self.reportId)
                res = self.client.last_received()
                #isGenerated = res.getChild("Envelope").getChild("Body").getChild('getReportStateResponse').getChild('isGenerated').getText()
                if isGenerated == 3:
                    break
        self.isGenerated = isGenerated
        log.info( "isGenerated:" + str(isGenerated))

        if isGenerated != 3:
            log.error('report generated with failure so exit')
            sys.exit(1)
        else:
            log.info('report generated successfully!')

    def __getReportFileUrl(self):
        if self.isGenerated == 3:
            reportFileUrl = self.client.service.getReportFileUrl(self.reportId)
            res = self.client.last_received()
            self.reportFileUrl = reportFileUrl
            log.info( "reportFileUrl:" + reportFileUrl)
            #printSoapResponse(res)
    #---------------------------------------------
    #genReport
    def __genReport(self):
        if self.request is not None:
            self.__getReportId()
            self.__getReportState()
            self.__getReportFileUrl()
        else:
            log.error("please gen request!")
            return

    def genAdgroupReport(self,startDate,endDate):
        self.genAdgroupRequest(startDate,endDate)
        self.__genReport()

    def genCampaignReport(self,startDate,endDate):
        self.genCampaignRequest(startDate,endDate)
        self.__genReport()

    def genKeywordReport(self,startDate,endDate):
        self.genKeywordRequest(startDate,endDate)
        self.__genReport()

    def genCreativeReport(self,startDate,endDate):
        self.genCreativeRequest(startDate,endDate)
        self.__genReport()

    def genRegionReport(self,startDate,endDate):
        self.genRegionRequest(startDate,endDate)
        self.__genReport()

    def genSiteReport(self,startDate,endDate):
        self.genSiteRequest(startDate,endDate)
        self.__genReport()

    def genIndustryReport(self,startDate,endDate):
        self.genIndustryRequest(startDate,endDate)
        self.__genReport()

    #-------------------------------------------
    def saveFileData(self,fileDirPath):
        startDate = self.requestParams['startDate']
        endDate = self.requestParams['endDate']
        startDateStr = datetime.strftime(startDate,'%Y%m%d')
        endDateStr = datetime.strftime(endDate,'%Y%m%d')

        fileName = "dsp-baidu"+'-'+self.reportTypeDesc+'.csv'
        filePath = os.path.join(fileDirPath,fileName)
        fileData=urlopen(self.reportFileUrl).read()
        f = file(filePath,"wb")
        f.write(fileData)
        f.close()
        self.filePath = filePath
        log.info( "save data into file:"+filePath)

    def getReport(self,reportType,startDate,endDate,fileDirPath):

        genReportFun = {
            'Campaign':self.genCampaignReport,
            'Adgroup':self.genAdgroupReport,
            'Keyword':self.genKeywordReport,
            'Creative':self.genCreativeReport,
            'Region':self.genRegionReport,
            'Site':self.genSiteReport,
            'Industry':self.genIndustryReport
        }

        if reportType in  genReportFun.keys():
            genReportFun.get(reportType)(startDate,endDate)

        else:
            log.error("please input correct reportType(such as Adgroup,Keyword,Region)!")
            return(-1)
        self.saveFileData(fileDirPath)




if __name__ == "__main__":  #only for test

    report = Report()

    startDate = datetime(2014,8,7)
    endDate = datetime(2014,8,8)

    report.genAdgroupReport(startDate,endDate)
    report.saveFileData('/home/robin/')

    ####parse
    parseReport = ReportParser(report)


    for rowDict in parseReport.parseCsvFileBody():
        save_report(rowDict)





