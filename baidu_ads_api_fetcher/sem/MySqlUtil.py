#coding=utf-8
import csv
import datetime
import MySQLdb
from string import Template

# TODO (robin): add create_date
# TODO (robin): campaignName-->loupan
# TODO (robin): date split
# TODO (robin): Refactoring

class SQLTemplate(Template):
    """docstring for SQLTemplate"""
    delimiter = '#'
class Table():
    def __init__(self,tableName,needUpdate=False):
        self.tableName = tableName
        self.needUpdate = needUpdate
        self.fields = None
        self.sqlStrDict ={}

    def setFields(self,fields):
        self.fields = fields

class MySqlUtil():
    def __init__(self):
        self.conn = MySQLdb.connect(host ='127.0.0.1',
                               port =3306,
                               db   ='etl',
                               user ='root',
                               passwd='zhitou',
                               charset='utf8')
        self.curs = self.conn.cursor()

        self.sqlStr={}


        self.TableList=({'report':Table('t_baidu_sem_report',True),
                        'account':Table('t_baidu_sem_account'),
                        'campaign':Table('t_baidu_sem_campaign'),
                        'adgroup':Table('t_baidu_sem_adgroup'),
                        'keyword':Table('t_baidu_sem_keyword'),
                        'creative':Table('t_baidu_sem_creative'),
                        'region':Table('t_baidu_sem_region')
                        })
        Fields = ['id', 'create_date', 'date', 'accountId', 'campaignId', 'adgroupId', 'keywordId', 'wordId', 'creativeId', 'regionId', 'impression', 'click', 'cost', 'cpc', 'ctr', 'cpm', 'device','unitOfTime', 'report_typ']
        self.TableList['report'].setFields(Fields)

        Fields = ['accountId','account']
        self.TableList['account'].setFields(Fields)

        Fields = ['campaignId','campaignName']
        self.TableList['campaign'].setFields(Fields)

        Fields = ['adgroupId','adgroupName']
        self.TableList['adgroup'].setFields(Fields)

        Fields = ['keywordId', 'wordId', 'keyword']
        self.TableList['keyword'].setFields(Fields)

        Fields = ['creativeId', 'title', 'description1','description2']
        self.TableList['creative'].setFields(Fields)

        Fields = ['regionId', 'region']
        self.TableList['region'].setFields(Fields)

    def setReportType(self,reportType,reportTypeDesc):
        self.reportType = reportType
        self.reportTypeDesc = reportTypeDesc
    def initAllSqlStr(self,csvHeadCode):
         for table in self.TableList.values():
            self.initSqlStr(csvHeadCode,table)

    def initSqlStr(self,csvHeadCode,Table ):
        self.reportTableName = Table.tableName
        csvHeadCode = list(set(csvHeadCode)&set(Table.fields))

        if csvHeadCode ==[]:
            self.sqlStr[Table.tableName]={}
            return

        performanceTotalSet = set(['cost', 'cpc', 'click', 'impression', 'ctr', 'cpm'])
        dimensionIdTotalList = set(['accountId','campaignId','adgroupId','keywordId','creativeId','regionId'])

        dimensionListIdOnly = list(set(csvHeadCode)&(dimensionIdTotalList|set(['date','device','unitOfTime','report_typ'])))  #idOnly:True
        dimensionList = list(set(csvHeadCode)-performanceTotalSet)                         #idOnly:False
        dimensionNameList = list(set(dimensionList)-set(dimensionListIdOnly))

        if Table.tableName == 't_baidu_sem_report':
            dimensionList = dimensionListIdOnly
            performanceList = list(set(csvHeadCode)&performanceTotalSet)
        else:
            dimensionList = dimensionListIdOnly
            performanceList = dimensionNameList

        #-----------------------------------------------------------
        sqlSelectWhereStr = ' where '+' and '.join([item+"='#"+item+"'" for item in dimensionList])
        sqlSelectStr = "SELECT id FROM " + self.reportTableName + sqlSelectWhereStr

        if len(performanceList) == 0:
            sqlInsertTableStr = "INSERT INTO " + self.reportTableName + \
                                '('+ ','.join([item for item in dimensionList]) +')'

            sqlInsertValuesStr = " VALUES(" + ','.join(["'#"+item+"'" for item in dimensionList]) +')'
        else:
            sqlInsertTableStr = "INSERT INTO " + self.reportTableName + \
                                '('+ ','.join([item for item in dimensionList]) + ',' + ','.join([item for item in performanceList])+')'

            sqlInsertValuesStr = " VALUES(" + ','.join(["'#"+item+"'" for item in dimensionList]) \
                                 + ',' + ','.join(["'#"+item+"'" for item in performanceList])+')'


        sqlInsertStr = sqlInsertTableStr +sqlInsertValuesStr

        sqlUpdateSetStr = " SET  " + ','.join([item+"= '#"+item+"'" for item in performanceList])

        sqlUpdateWhereStr = " WHERE id = %s"

        sqlUpdateStr = "UPDATE "+ self.reportTableName + sqlUpdateSetStr + sqlUpdateWhereStr

        sqlStrDict ={}
        sqlStrDict['sqlSelectStr'] = SQLTemplate(sqlSelectStr)
        sqlStrDict['sqlInsertStr'] = SQLTemplate(sqlInsertStr)
        sqlStrDict['sqlUpdateStr'] = SQLTemplate(sqlUpdateStr)

        self.sqlStr[Table.tableName]= sqlStrDict

        #print(sqlSelectStr)
        #print(sqlInsertStr)
        #print(sqlUpdateStr)

    def updateTable(self,rowDict,Table):
        tableName = Table.tableName

        #sqlSelectStr = self.sqlSelectStr.substitute(rowDict)
        sqlSelectStr = self.sqlStr[tableName]['sqlSelectStr'].substitute(rowDict)

        self.curs.execute(sqlSelectStr)
        result = self.curs.fetchone()
        if result is None:
            #sqlInsertStr = self.sqlInsertStr.substitute(rowDict)
            sqlInsertStr = self.sqlStr[tableName]['sqlInsertStr'].substitute(rowDict)
            self.curs.execute(sqlInsertStr)
            self.conn.commit()
        elif Table.needUpdate:
            #sqlUpdateStr = self.sqlUpdateStr.substitute(rowDict)
            sqlUpdateStr = self.sqlStr[tableName]['sqlUpdateStr'].substitute(rowDict)

            sqlUpdateStr = sqlUpdateStr %(result[0])
            self.curs.execute(sqlUpdateStr)
            self.conn.commit()

    def mergeReprtToDb(self,rowDict):
        for table in self.TableList.values():
            if self.sqlStr[table.tableName]!={}:
                self.updateTable(rowDict,table)


if __name__ == "__main__":  #for test

    mysqlConn = MySqlUtil()
    mysqlConn.setReportType(11,'AdGroup')
    csvHeadCode = ['date', 'accountId', 'account', 'campaignId', 'campaignName', 'adgroupId', 'adgroupName', 'impression', 'click', 'cost', 'cpc']
    #csvHeadCode.append('device')
    csvHeadCode.append('report_typ')

    rowDict={'account': 'baidu-\xe6\x88\xbf\xe5\xa4\x9a\xe5\xa4\x9a-\xe4\xb8\x8a\xe6\xb5\xb78131931', 'impression': '66', 'adgroupId': '536529173', 'adgroupName': '\xe5\x9f\x8e\xe5\xb8\x82\xe5\x93\x81\xe7\x89\x8c\xe8\xaf\x8d', 'campaignId': '16690006', 'cpc': '1.75', 'click': '10', 'cost': '17.47', 'campaignName': '\xe6\x98\x86\xe6\x98\x8e-\xe5\xae\x9e\xe5\x8a\x9b\xe5\xa3\xb9\xe6\x96\xb9\xe5\x9f\x8e-\xe5\x85\xa8\xe5\x9b\xbd', 'date': '2014-08-07', 'accountId': '7034363'}

    #rowDict['device']='pc'
    rowDict['report_typ']='adGroup'
    mysqlConn.initAllSqlStr(csvHeadCode)
    mysqlConn.mergeReprtToDb(rowDict)

