#coding=utf-8

import sys
import csv

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class ReportParser(object):

    def __init__(self,filePath):
        self.filePath = filePath
        #self.filePath = report.filePath
        #self.reportType = report.requestParams['reportType']
        #self.reportTypeDesc = report.reportTypeDesc
        self.csvHead={}
        self.colIndex={}
        self.__init_mapping()
        self.inverseMapping=dict([(value,key) for key,value in self.mapping.items()])
        self.parseCsvFileHead()

    def __init_mapping(self):
        self.mapping={}
        self.mapping['date']='日期'
        self.mapping['accountid']='账户ID'
        self.mapping['account']='账户'
        self.mapping['campaignid']='推广计划ID'
        self.mapping['campaigname']='推广计划'

        self.mapping['adgroupid']='推广组ID'
        self.mapping['adgroupname']='推广组'

        self.mapping['keywordid']='关键词keywordID'
        self.mapping['wordid']='关键词ID'
        self.mapping['keyword']='关键词'

        self.mapping['creativeid']='创意ID'
        self.mapping['title']='创意标题'
        self.mapping['creativetype']='创意类型'
        self.mapping['description1']='创意描述1'
        self.mapping['description2']='创意描述2'

        self.mapping['regionid']='地域ID'
        self.mapping['region']='地域'
        self.mapping['regiontype']='地域类型'
        self.mapping['regionid1']='一级地域ID'

        self.mapping['impression']='展现'
        self.mapping['click']='点击'
        self.mapping['cost']='消费'
        self.mapping['cpc']='平均点击价格'
        self.mapping['ctr']='CTR'
        self.mapping['cpm']='CPM'
        self.mapping['cpm']='CPM'
        self.mapping['CTR']='CTR'
        self.mapping['CPM']='CPM'
        self.mapping['ACP']='ACP'

    def parseCsvFileHead(self):
        try:
            with open(self.filePath, 'rb') as csvfile:
                csvreader = csv.reader(csvfile, delimiter='\t')
                rownum = 0
                for row in csvreader:
                    for i in range(len(row)):
                        self.csvHead[i]=row[i]#.decode('gbk').encode('utf-8')
                        self.colIndex[self.csvHead[i]]= i
                    self.csvHeadCode = [self.inverseMapping[value]   for value in self.csvHead.values()]
                    break
        except Exception, e:
            print e

    def parseCsvFileBody(self):


        try:
            with open(self.filePath, 'rb') as csvfile:
                csvreader = csv.reader(csvfile, delimiter='\t')
                rownum = 0
                for row in csvreader:
                    rowDict = {}
                    if (rownum == 0):
                        rownum = rownum + 1
                        continue
                    for i in range(len(row)):
                        rowDict[self.csvHead[i]] = row[i] #.decode('gbk').encode('utf-8')
                        rownum = rownum + 1
                        currRowDict = dict([(self.inverseMapping[key],value) for key,value in rowDict.items()])
                    yield currRowDict

        except Exception, e:
            print e
    def parseCsvFile(self):

        for rowDict in self.parseCsvFileBody():
            print rowDict

if __name__ == "__main__":

    ReportParser()
