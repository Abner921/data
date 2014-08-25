#encoding=utf-8
from sms_v3_ReportService import *
import time
import os
from datetime import datetime,date,timedelta
from ApiSDKSoapClient import ApiSDKSoapClient
from ApiSDKSoapClient import printSoapResponse
from PreviewUtil import *
from urllib import urlopen

from ReportParser import ReportParser
from Contants import Contants


import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# TODO (robin): define constants
# TODO (robin): contition filter
# TODO (robin): csv parse
# TODO (robin): import data into DB
# TODO (robin): add realtime report
# TODO (robin): design function and params
# TODO (robin): add logs
# TODO (robin): github

class Report():

    def __init__(self,userid):
        self.userid = userid
        apiSDKSoapClient = ApiSDKSoapClient('sms','v3','ReportService',userid)
        newClient = apiSDKSoapClient.newSoapClient()
        self.client = newClient
        self.requestParams={}
        self.request = None
        self.reportTypeDesc = None
        self.__init_requestParams()

    def __init_requestParams(self):
        
        self.requestParams['performanceData']= ['cost','impression','click','cpc']
        #self.requestParams['startDate'] = startDate
        #self.requestParams['endDate'] = endDate
        self.requestParams['idOnly'] = False
        #self.requestParams['levelOfDetails'] = 7
        #self.requestParams['reportType'] = 12
        self.requestParams['format'] = 2  #csv
        self.requestParams['statRange'] = 2
        self.requestParams['unitOfTime'] = 5
        self.requestParams['device'] = 0
        
    def setRequestParamsDevice(self,device):
        self.requestParams['device'] = device
    def setRequestParamUnitOfTime(self,unitOfTime):
        self.requestParams['unitOfTime'] = unitOfTime
    def setRequestParamStatRange(self,statRange):
        self.requestParams['statRange'] = statRange
    def setRequestParamIdOnly(self,idOnly):
        self.requestParams['idOnly'] = idOnly

    def __genRequest(self):
        request = self.client.factory.create('getProfessionalReportIdRequest')
        reportRequestType = self.client.factory.create('getProfessionalReportIdRequest.reportRequestType')

        reportRequestType.performanceData = self.requestParams['performanceData']
        reportRequestType.startDate       = self.requestParams['startDate']
        reportRequestType.endDate         = self.requestParams['endDate']
        reportRequestType.idOnly          = self.requestParams['idOnly'] #
        reportRequestType.levelOfDetails  = self.requestParams['levelOfDetails']
        reportRequestType.reportType      = self.requestParams['reportType']
        reportRequestType.format          = self.requestParams['format']  # 2:csv
        reportRequestType.statRange       = self.requestParams['statRange']   #统计粒度  2：账户范围 3：计划范围 5：单元范围
        reportRequestType.unitOfTime      = self.requestParams['unitOfTime'] #统计时间单位 5：日报 4：周报 3：月报 1：年报 7：小时报
        reportRequestType.device          = self.requestParams['device']  # 0:pc and mobile  1:pc 2:mobile
        request.reportRequestType = reportRequestType
        self.request = request

    def genCampaignRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Campaign'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['levelOfDetails'] = 3
        self.requestParams['reportType'] = 10
        # statRange : 2, 3 (账户范围,计划范围)
        # unitOfTime: 1,3,4,5,7,8 (年报,月报,周报,日报,小旪报,请求旪间段汇总)
        self.__genRequest()

    def genAdgroupRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Adgroup'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['levelOfDetails'] = 5
        self.requestParams['reportType'] = 11
        # statRange : 2, 3, 5 (账户范围,计划范围,单元范围)
        # unitOfTime: 1,3,4,5,8 (年报,月报,周报,日报,请求旪间段汇总)

        self.__genRequest()

    def genKeywordRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Keyword'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['levelOfDetails'] = 11
        self.requestParams['reportType'] = 14
        # statRange : 2, 3, 5,11(账户范围,计划范围,单元范围,关键词 keywordid 范围)
        # unitOfTime: 1,3,4,5,8 (年报,月报,周报,日报,请求旪间段汇总)
        self.__genRequest()

    def genCreativeRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Creative'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['levelOfDetails'] = 7
        self.requestParams['reportType'] = 12
        # statRange : 2, 3, 5, 7(账户范围,计划范围,单元范围,创意范围)
        # unitOfTime: 1,3,4,5,8 (年报,月报,周报,日报,请求旪间段汇总)
        self.__genRequest()

    def genWordRequest(self,startDate,endDate):
        self.reportTypeDesc = 'Word'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['levelOfDetails'] = 6
        self.requestParams['reportType'] = 9
        # statRange : 2, 3, 5,11(账户范围,计划范围,单元范围,关键词 keywordid 范围)
        # unitOfTime: 1,3,4,5,8 (年报,月报,周报,日报,请求旪间段汇总)
        self.__genRequest()

    def genRegionRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Region'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['levelOfDetails'] = 5
        self.requestParams['reportType'] = 3
        # statRange : 2, 3, 5(账户范围,计划范围,单元范围)
        # unitOfTime: 1,3,4,5,8 (年报,月报,周报,日报,请求旪间段汇总)
        self.__genRequest()

    #搜索词报告  当天中午 11:51 后获取昨天数据
    #搜索词的旪间跨度不超过 31 天 !!!
    def genSearchWordRequest(self,startDate,endDate):
        #some tips
        if (startDate < datetime.today()-timedelta(days=31)):
            print "startDate not allowed."
            return
        self.reportTypeDesc = 'SearchWord'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['levelOfDetails'] = 12
        #levelOfDetails:7 (创意粒度) 12(关键词+创意维度,选择此维度您能获取搜索词所触发的关键词)
        self.requestParams['reportType'] = 6
        self.requestParams['performanceData']= ['impression','click']
        # statRange : 2, 3(账户范围,计划范围)
        # unitOfTime: 5,8 (日报,请求旪间段汇总)
        self.__genRequest()

    #匹配报告
    def genMatchRequest(self,startDate,endDate):

        self.reportTypeDesc = 'Match'
        self.requestParams['startDate'] = startDate
        self.requestParams['endDate'] = endDate
        self.requestParams['levelOfDetails'] = 12
        #levelOfDetails:7 (创意粒度) 12(关键词+创意维度,选择此维度您能获取搜索词所触发的关键词)
        self.requestParams['reportType'] = 15
        # statRange :2, 3, 5,7,11(账户范围,计划范围,单元范围,创意范围,关键词 keywordid 范围)
        # unitOfTime: 1,3,4,5,8 (年报,月报,周报,日报,请求旪间段汇总)

        self.__genRequest()
    #
    def genRealTimeDataRequest(self):
        #realtime
        pass
    #----------------------------------
    def __getProfessionalReportId(self):
        reportId=self.client.service.getProfessionalReportId(self.request.reportRequestType)
        res = self.client.last_received()
        self.reportId = reportId
        #reportId=res.getChild("Envelope").getChild("Body").getChild('getProfessionalReportIdResponse').getChild('reportId').getText()
        #printSoapResponse(res)
        print "reportId:" + reportId

    def __getReportState(self):
        isGenerated = self.client.service.getReportState(self.reportId)
        res = self.client.last_received()
        #isGenerated = res.getChild("Envelope").getChild("Body").getChild('getReportStateResponse').getChild('isGenerated').getText()

        if (isGenerated != 3):
            for i in range(1, 5):
                time.sleep(10)
                isGenerated = self.client.service.getReportState(self.reportId)
                res = self.client.last_received()
                #isGenerated = res.getChild("Envelope").getChild("Body").getChild('getReportStateResponse').getChild('isGenerated').getText()
                if isGenerated == 3:
                    break
        self.isGenerated = isGenerated
        print "isGenerated:" + str(isGenerated)

    def __getReportFileUrl(self):
        if self.isGenerated == 3:
            reportFileUrl = self.client.service.getReportFileUrl(self.reportId)
            res = self.client.last_received()
            #reportFileUrl= res.getChild("Envelope").getChild("Body").getChild('getReportFileUrlResponse').getChild('reportFilePath').getText()
            self.reportFileUrl = reportFileUrl
            print "reportFileUrl:" + reportFileUrl
            #printSoapResponse(res)
    #---------------------------------------------
    #genReport
    def __genReport(self):
        if self.request is not None:
            self.__getProfessionalReportId()
            self.__getReportState()
            self.__getReportFileUrl()
        else:
            print("please gen request!")
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

    def genSearchWordReport(self,startDate,endDate):
        self.genSearchWordRequest(startDate,endDate)
        self.__genReport()

    def genMatchReport(self,startDate,endDate):
        self.genMatchRequest(startDate,endDate)
        self.__genReport()

    #-------------------------------------------
    def saveFileData(self,fileDirPath):
        startDate = self.requestParams['startDate']
        endDate = self.requestParams['endDate']
        startDateStr = datetime.strftime(startDate,'%Y%m%d')
        endDateStr = datetime.strftime(endDate,'%Y%m%d')
        device = self.requestParams['device']
        #fileName = self.reportTypeDesc+'_'+str(device)+'['+startDateStr+'-'+endDateStr+'].csv'
        fileName = "sem-baidu"+'-'+self.userid+'-'+Contants.deviceName[device]+'-'+self.reportTypeDesc+'.csv'
        filePath = os.path.join(fileDirPath,fileName)
        fileData=urlopen(self.reportFileUrl).read()
        f = file(filePath,"wb")
        f.write(fileData)
        f.close()
        self.filePath = filePath
        print "save data into file:"+filePath

    def getReport(self,reportType,startDate,endDate,fileDirPath,device=0,unitOfTime=7):

        self.setRequestParamsDevice(device)
        self.setRequestParamUnitOfTime(unitOfTime)

        genReportFun = {
            'Campaign':self.genCampaignReport,
            'Adgroup':self.genAdgroupReport,
            'Keyword':self.genKeywordReport,
            'Creative':self.genCreativeReport,
            'Region':self.genRegionReport,
            'Search':self.genSearchWordReport,
            'Match':self.genMatchReport
        }

        if reportType in  genReportFun.keys():
            genReportFun.get(reportType)(startDate,endDate)

        else:
            print("please input correct reportType(such as Adgroup,Keyword,Region)!")
            return(-1)
        self.saveFileData(fileDirPath)




if __name__ == "__main__":  #for test

    report = Report()

    startDate = datetime(2014,8,7)
    endDate = datetime(2014,8,8)

    report.genAdgroupReport(startDate,endDate)
    report.saveFileData('/home/robin/')

    ####parse
    parseReport = ReportParser(report)

    ##






