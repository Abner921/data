#coding=utf-8
import pymongo
conn = pymongo.Connection('192.168.9.102', 27017)

#TODO:update document

db = conn.fdd_ads
reports = db.baidu_sem_raw


def save_report(rowDict):

    keyFields = ['id','date', 'accountId', 'campaignId', 'adgroupId',
                 'keywordId', 'wordId', 'creativeId', 'regionId',
                 'device','unitOfTime','deviceId','unitOfTimeId','deviceName','unitOfTimeName', 'reportType']
    performanceFields= ['createDate','impression', 'click', 'cost', 'cpc', 'ctr', 'cpm']  #'create_date' need update

    keys = rowDict.keys()
    values = rowDict.values()

    keyDict = dict([(key,rowDict[key])  for key in set(keys)&set(keyFields)])
    performanceDict = dict([(key,rowDict[key])  for key in set(keys)-set(keyFields)])

    reports.update(keyDict , { '$set' : performanceDict },upsert=True,multi= False )
  #  reports.insert(rowDict)

if __name__ == "__main__":
    rowDict={'account': 'baidu-\xe6\x88\xbf\xe5\xa4\x9a\xe5\xa4\x9a-\xe4\xb8\x8a\xe6\xb5\xb78131931', 'impression': '66', 'adgroupId': '536529173', 'adgroupName': '\xe5\x9f\x8e\xe5\xb8\x82\xe5\x93\x81\xe7\x89\x8c\xe8\xaf\x8d', 'campaignId': '16690006', 'cpc': '1.75', 'click': '10', 'cost': '17.47', 'campaignName': '\xe6\x98\x86\xe6\x98\x8e-\xe5\xae\x9e\xe5\x8a\x9b\xe5\xa3\xb9\xe6\x96\xb9\xe5\x9f\x8e-\xe5\x85\xa8\xe5\x9b\xbd', 'date': '2014-08-07', 'accountId': '7034363'}
    rowDict['report_typ']='keyword'
    save_report(rowDict)



