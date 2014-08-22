import suds
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse

if __name__ == "__main__":
    try:
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('AdService')
        client = baiduApiSoap.client

		#==== add ad ====
        # contruct request body
        request = client.factory.create('addAdRequest')
        ad = client.factory.create('addAdRequest.adTypes')
        ad.localId = 1
        ad.groupId = 2166166
        ad.status = 0
        ad.type = 2
        ad.title = 'test_title1234567'
        ad.displayUrl = 'baidu.com'
        ad.destinationUrl = 'http://baidu.com/123'
        ad.description1 = 'desc1234567'
        ad.description2 = 'desc2345678'
        request.adTypes = []
        request.adTypes.append(ad)

        # send request
        client.service.addAd(request.adTypes)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)

        #==== update ad ====
        # send request
        ad.title = 'test_update_title_123456'
        client.service.updateAd(request.adTypes)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)

		#==== get ad by id====
        # send request
        adIds = []
        adIds.append(9283659)
        client.service.getAdByAdId(adIds)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)


        #==== set ad status ====
        # contruct request body
        request = client.factory.create('setAdStatusRequest')
        s = client.factory.create('setAdStatusRequest.statusTypes')
        s.adId = 9283659
        s.status = 1
        request.statusTypes = []
        request.statusTypes.append(s)
        print request
        # send request
        client.service.setAdStatus(request.statusTypes)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
    except Exception, e:
        print e
        tb.print_exc()

