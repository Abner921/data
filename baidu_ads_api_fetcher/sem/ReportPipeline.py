#!/usr/bin/python
#encoding=utf-8
from GetReport import Report
from ReportParser import ReportParser
from MySqlUtil import MySqlUtil
from datetime import datetime
from datetime import date, timedelta
import sys,os
from optparse import OptionParser
from MongoUtil import save_report


def fetchReport(reportType,startDate,endDate,fileDirPath,device,unitOfTime):

    report = Report()
    report.getReport(reportType,startDate,endDate,fileDirPath,device,unitOfTime)
    ####parse csv
    device = report.requestParams['device']
    unitOfTime = report.requestParams['unitOfTime']
    parseReport = ReportParser(report)

    for rowDict in parseReport.parseCsvFileBody():
        save_report(rowDict)
    ##import into db
    '''
    mysqlConn = MySqlUtil()
    csvHeadCode = parseReport.csvHeadCode
    csvHeadCode.append('device')
    csvHeadCode.append('report_typ')
    csvHeadCode.append('unitOfTime')
    mysqlConn.initAllSqlStr(csvHeadCode)

    for rowDict in parseReport.parseCsvFileBody():
        rowDict['device']= device
        rowDict['report_typ']=reportType
        rowDict['unitOfTime']=unitOfTime
        mysqlConn.mergeReprtToDb(rowDict)
        '''
def test():
    yesterdayStr = (date.today()-timedelta(1)).strftime('%Y-%m-%d')
    yesterday = datetime.strptime(yesterdayStr,'%Y-%m-%d')

    baseDir = os.path.dirname(os.path.dirname(__file__))
    dataDirPath = os.path.join(baseDir,'data',yesterday.strftime('%Y-%m/%d'))

    if not os.path.isdir(fileDirPath):
        os.makedirs(fileDirPath)

    startDate = datetime(2014,5,7)
    endDate = datetime(2014,5,8)
    #reportType = 'Campaign'
    reportType = 'Keyword'
    fetchReport(reportType,startDate,endDate,fileDirPath)


if __name__ == "__main__":
    yesterdayStr = (date.today()-timedelta(1)).strftime('%Y-%m-%d')
    yesterday = datetime.strptime(yesterdayStr,'%Y-%m-%d')


    baseDir = os.path.dirname(os.path.dirname(__file__))
    dataDirPath = os.path.join(baseDir,'data',yesterday.strftime('%Y-%m/%d'))

    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser()

    parser.add_option("-r", "--report", action="store",dest="reportType",help="reportType", default="Keyword")
    parser.add_option("-s","--start", action="store", dest="startDate", default=yesterdayStr)
    parser.add_option("-e", "--end",action="store", dest="endDate",default=yesterdayStr)

    parser.add_option("-p", "--path",action="store", dest="fileDirPath",default=dataDirPath)
    parser.add_option("-d", "--device",action="store",type="int", dest="device",default=1)
    parser.add_option("-u", "--unit",action="store",type="int", dest="unitOfTime",default=5)
    (options, args) = parser.parse_args()


    reportType = options.reportType
    startDate = datetime.strptime(options.startDate,'%Y-%m-%d')
    endDate = datetime.strptime(options.endDate,'%Y-%m-%d')
    fileDirPath = options.fileDirPath
    device = options.device
    unitOfTime = options.unitOfTime

    if not os.path.isdir(fileDirPath):
        os.makedirs(fileDirPath)

    fetchReport(reportType,startDate,endDate,fileDirPath,device,unitOfTime)