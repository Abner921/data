#!/usr/bin/python
#encoding=utf-8
from GetReport import Report
from ReportParser import ReportParser
from datetime import datetime
from datetime import date, timedelta
import sys,os
from optparse import OptionParser
from MongoUtil import save_report
from LoggingUtil import getLogger

log = getLogger()

def fetchReport(reportType,startDate,endDate,fileDirPath):

    report = Report()
    report.getReport(reportType,startDate,endDate,fileDirPath)
    ####parse csv

    parseReport = ReportParser(report)

    ##import into db
    for rowDict in parseReport.parseCsvFileBody():

        rowDict['reportType']=reportType
        rowDict['createDate']=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        save_report(rowDict)
    log.info('save data into mongodb successful.')

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


    baseDir = os.path.split(os.path.realpath(__file__))[0]
    dataDirPath = os.path.join(baseDir,'..','data',yesterday.strftime('%Y-%m/%d'))

    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser()

    parser.add_option("-r", "--report", action="store",dest="reportType",help="Keyword|Campaign|Region", default="Keyword")
    parser.add_option("-s","--start", action="store", dest="startDate", default=yesterdayStr)
    parser.add_option("-e", "--end",action="store", dest="endDate",default=yesterdayStr)
    parser.add_option("-p", "--path",action="store", dest="fileDirPath",default=dataDirPath)

    (options, args) = parser.parse_args()


    reportType = options.reportType
    startDate = datetime.strptime(options.startDate,'%Y-%m-%d')
    endDate = datetime.strptime(options.endDate,'%Y-%m-%d')
    fileDirPath = options.fileDirPath

    log.debug("fileDirPath:"+fileDirPath)

    if not os.path.isdir(fileDirPath):
        os.makedirs(fileDirPath)

    fetchReport(reportType,startDate,endDate,fileDirPath)