#!/usr/bin/python
#encoding=utf-8
from GetReport import Report
from ReportParser import ReportParser
from datetime import datetime
from datetime import date, timedelta
import sys,os
from optparse import OptionParser
from MongoUtil import save_report
from Contants import Contants

def fetchReport(reportType,startDate,endDate,fileDirPath,device,unitOfTime):

    report = Report()
    report.getReport(reportType,startDate,endDate,fileDirPath,device,unitOfTime)
    ####parse csv
    device = report.requestParams['device']
    unitOfTime = report.requestParams['unitOfTime']
    parseReport = ReportParser(report)

    ##import into db
    for rowDict in parseReport.parseCsvFileBody():
        rowDict['deviceName']= Contants.deviceName[device]
        rowDict['deviceId']= device
        rowDict['reportType']=reportType
        rowDict['unitOfTimeName']= Contants.unitOfTimeName[unitOfTime]
        rowDict['unitOfTimeId']=unitOfTime
        rowDict['createDate']=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        save_report(rowDict)


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

    parser.add_option("-r", "--report", action="store",dest="reportType",help="Keyword|Campaign|Region", default="Keyword")
    parser.add_option("-s","--start", action="store", dest="startDate", default=yesterdayStr)
    parser.add_option("-e", "--end",action="store", dest="endDate",default=yesterdayStr)
    parser.add_option("-p", "--path",action="store", dest="fileDirPath",default=dataDirPath)

    parser.add_option("-d", "--device",action="store",type="string", dest="deviceName",default="pc",help="pc|mobile|all")
    parser.add_option("-u", "--unit",action="store",type="string", dest="unitOfTimeName",default="day",help="year|month|day|week|hour|period")
    (options, args) = parser.parse_args()


    reportType = options.reportType
    startDate = datetime.strptime(options.startDate,'%Y-%m-%d')
    endDate = datetime.strptime(options.endDate,'%Y-%m-%d')
    fileDirPath = options.fileDirPath

    device = Contants.deviceId[options.deviceName]
    unitOfTime = Contants.unitOfTimeId[options.unitOfTimeName]

    if not os.path.isdir(fileDirPath):
        os.makedirs(fileDirPath)

    fetchReport(reportType,startDate,endDate,fileDirPath,device,unitOfTime)