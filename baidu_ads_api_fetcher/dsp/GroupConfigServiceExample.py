import suds
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse
import re

if __name__ == "__main__":
    try:
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('GroupConfigService')
        client = baiduApiSoap.client

#        """
#        set target to kt
#        """
#        # contruct request body
#        request = client.factory.create('setTargetInfoRequest')
#        targetInfo = client.factory.create('setTargetInfoRequest.targetInfo')
#        targetInfo.type = 2
#        targetInfo.groupId = 228
#        ktItem = client.factory.create('setTargetInfoRequest.targetInfo.ktItem')
#        ktItem.aliveDays = 30
#        ktItem.targetType = 7
#        ktWordList1 = client.factory.create('setTargetInfoRequest.targetInfo.ktItem.ktWordList')
#        ktWordList1.keyword = 'baidu-search'
#        ktWordList1.pattern = 0
#        ktWordList1.qualification = 1
#        ktWordList2 = client.factory.create('setTargetInfoRequest.targetInfo.ktItem.ktWordList')
#        ktWordList2.keyword = 'baidu-union'
#        ktWordList2.pattern = 1
#        ktWordList2.qualification = 3
#        ktItem.ktWordList = []
#        ktItem.ktWordList.append(ktWordList1)
#        ktItem.ktWordList.append(ktWordList2)
#        targetInfo.ktItem = ktItem
#        targetInfo.rtItem = None
#        targetInfo.vtItem = None
#        request.targetInfo = targetInfo
#
#        # send request
#        client.service.setTargetInfo(request.targetInfo)
#        
#        # receive response and print result
#        res = client.last_received()
#        printSoapResponse(res)
#
#        """
#        get target info
#        """
#        # contruct request body
#        request = client.factory.create('getTargetInfoRequest')
#        request.groupIds = [228]
#        # send request
#        client.service.getTargetInfo(request.groupIds)
#        
#        # receive response and print result
#        res = client.last_received()
#        printSoapResponse(res)
#
#        """
#        get keyword by keywordId
#        """
#        # contruct request body
#        request = client.factory.create('getKeywordRequest')
#        request.keywordIds = [123456]
#        # send request
#        reportId = client.service.getKeyword(request.keywordIds)
#        
#        # receive response and print result
#        res = client.last_received()
#        printSoapResponse(res)
#        
#        """
#        add keyword
#        """
#        # contruct request body
#        request = client.factory.create('addKeywordRequest')
#        ktWordList1 = client.factory.create('addKeywordRequest.keywords')
#        ktWordList1.keyword = 'baidu-ad123'
#        ktWordList1.pattern = 1
#        ktWordList1.groupId = 228
#        ktWordList2 = client.factory.create('addKeywordRequest.keywords')
#        ktWordList2.keyword = 'baidu-mp3'
#        ktWordList2.pattern = 1
#        ktWordList2.groupId = 228
#        request.keywords = []
#        request.keywords.append(ktWordList1)
#        request.keywords.append(ktWordList2)
#        print request
#        
#        # send request
#        client.service.addKeyword(request.keywords)
#        
#        # receive response and print result
#        res = client.last_received()
#        printSoapResponse(res)
#        
#        """
#        delete keyword
#        """
#        # contruct request body
#        request = client.factory.create('deleteKeywordRequest')
#        ktWordList1 = client.factory.create('deleteKeywordRequest.keywords')
#        ktWordList1.keyword = 'baidu-ad123'
#        ktWordList1.pattern = 1
#        ktWordList1.groupId = 228
#        request.keywords = []
#        request.keywords.append(ktWordList1)
#        print request
#        
#        # send request
#        client.service.deleteKeyword(request.keywords)
#        
#        # receive response and print result
#        res = client.last_received()
#        printSoapResponse(res)
#        
        """
        set interest info 
        """
        # contruct request body
        request = client.factory.create('setInterestInfoRequest')
        interestInfo = client.factory.create('setInterestInfoRequest.interestInfo')
        interestInfo.enable = True
        interestInfo.groupId = 228
        interestInfo.interestIds = []
        interestInfo.interestIds.append(2)
        interestInfo.interestIds.append(3)
        interestInfo.exceptInterestIds = []
        interestInfo.exceptInterestIds.append(602)
        request.interestInfo = interestInfo

        # send request
        client.service.setInterestInfo(request.interestInfo)
        
        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
        """
        get interest info
        """
        # contruct request body
        request = client.factory.create('getInterestInfoRequest')
        request.groupIds = [228]
        # send request
        client.service.getInterestInfo(request.groupIds)
        
        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
        """
        add interest info
        """
        # contruct request body
        request = client.factory.create('addInterestInfoRequest')
        itList1 = client.factory.create('addInterestInfoRequest.interests')
        itList1.interestIds = []
        itList1.interestIds.append(11)
        itList1.exceptInterestIds = None
        request.interests = []
        request.interests.append(itList1)
        print request
        
        # send request
        client.service.addInterestInfo(request.interests)
        
        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
        """
        delete interest info
        """
        # contruct request body
        request = client.factory.create('deleteInterestInfoRequest')
        itList1 = client.factory.create('deleteInterestInfoRequest.interests')
        itList1.interestIds = []
        itList1.interestIds.append(11)
        itList1.exceptInterestIds = []
        itList1.groupId = 228
        request.interests = []
        request.interests.append(itList1)
        
        # send request
        client.service.deleteInterestInfo(request.interests)
        
        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
        """
        set exclude ip
        """
        # contruct request body
        request = client.factory.create('setExcludeIpRequest')
        excludeIp = client.factory.create('setExcludeIpRequest.excludeIp')
        excludeIp.groupId = 228
        excludeIp.excludeIp = ['1.1.1.1', '2.2.2.2']
        request.excludeIp = excludeIp
        
        # send request
        client.service.setExcludeIp(request.excludeIp)
        
        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)

        """
        get exclude ip
        """
        # contruct request body
        request = client.factory.create('getExcludeIpRequest')
        request.groupIds = [228]
        # send request
        client.service.getExcludeIp(request.groupIds)
        print request
        
        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
    except Exception, e:
        print e
        tb.print_exc()

