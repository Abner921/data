import suds
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse

if __name__ == "__main__":
    try:
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('CodeService')
        client = baiduApiSoap.client

		#==== getAllCategory ====
        client.service.getAllCategory()

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)

        #==== getAllRegion ====
        client.service.getAllRegion()

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
    except Exception, e:
        print e
        tb.print_exc()

