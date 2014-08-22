import suds
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse

if __name__ == "__main__":
    try:
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('GroupService')
        client = baiduApiSoap.client

		#==== add group ====
        # contruct request body
        request = client.factory.create('addGroupRequest')
        group = client.factory.create('addGroupRequest.groupTypes')
        group.campaignId = 757456
        group.groupName = 'test123456'
        group.price = 200
        group.type = 0
        group.status = 0
        request.groupTypes = []
        request.groupTypes.append(group)

        # send request
        client.service.addGroup(request.groupTypes)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)


        #==== get group by campaign id====
        # send request
        campaignId = 108
        client.service.getGroupByCampaignId(campaignId)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
		#==== get group by id====
        # send request
        groupIds = []
        groupIds.append(2166166)
        client.service.getGroupByGroupId(groupIds)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
    except Exception, e:
        print e
        tb.print_exc()

