import suds
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse

if __name__ == "__main__":
    try:
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('InterestService')
        client = baiduApiSoap.client

		#==== get all system specified interests ====
        client.service.getInterest()

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)


        #==== get custom interests ====
        # send request
        client.service.getAllCustomInterest()

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
        #==== get custom interests ====
        # send request
        cids = [100109,100110]
        client.service.getCustomInterest(cids)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
    except Exception, e:
        print e
        tb.print_exc()

