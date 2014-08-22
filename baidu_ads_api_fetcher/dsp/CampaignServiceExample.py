import suds
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse

if __name__ == "__main__":
    try:
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('CampaignService')
        client = baiduApiSoap.client

		#==== add campaign====
        # contruct request body
        request = client.factory.create('addCampaignRequest')
        campaign = client.factory.create('addCampaignRequest.campaignTypes')
        campaign.campaignName = 'test123456'
        campaign.budget = 200
        campaign.status = 0
        request.campaignTypes = []
        request.campaignTypes.append(campaign)

        # send request
        client.service.addCampaign(request.campaignTypes)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
        #==== get all campaign id====
        # send request
        client.service.getCampaignId()

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)

		#==== get campaign by id====
        # send request
        campaignIds = []
        campaignIds.append(757446)
        client.service.getCampaignByCampaignId(campaignIds)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
    except Exception, e:
        print e
        tb.print_exc()

