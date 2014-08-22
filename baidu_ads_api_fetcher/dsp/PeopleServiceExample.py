import suds
import traceback as tb
from BaiduNmsApiClientHelper import BaiduNmsApiClient
from BaiduNmsApiClientHelper import printSoapResponse
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

if __name__ == "__main__":
    try:
        # init client stub
        baiduApiSoap = BaiduNmsApiClient('PeopleService')
        client = baiduApiSoap.client

		#==== get all people ====
        client.service.getAllPeople()

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)


        #==== set specified people ====
        # send request
        pids = [14,15,16]
        client.service.getPeople(pids)

        # receive response and print result
        res = client.last_received()
        printSoapResponse(res)
        
    except Exception, e:
        print e
        tb.print_exc()

