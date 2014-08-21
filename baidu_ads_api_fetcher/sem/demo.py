#coding=utf-8
from sms_v3_ReportService import *
import time
from datetime import datetime,date
from ApiSDKSoapClient import ApiSDKSoapClient
from PreviewUtil import *


if __name__ == "__main__":
    try:
        service =  sms_v3_ReportService()
        startDate = datetime(2014,4,7)
        endDate = datetime(2014,5,7)
        request = {"reportType":11,"startDate":startDate.__str__(),"endDate":endDate.__str__(),"levelOfDetails":5,"performanceData":['cost','cpc','click','impression']}
       # request = {"performanceData":['cost','cpc','click','impression'],"startDate":startDate,"endDate":endDate,\
      #            "idOnly":False,"levelOfDetails":5,"reportType":11,"format":2,"statRange":2,"unitOfTime":5,"device":0}


        '''
        reportid = service.getProfessionalReportId({
            "reportType":11,
            "startDate":'2014-05-10T00:00:00.000',
            "idOnly":True,
            "endDate":'2014-05-15T00:00:00.000',
            "performanceData":['impression'],"levelOfDetails":5})
            '''
        reportid = service.getProfessionalReportId(request)
        print "report id: "+ str(reportid)
        isGenerated = service.getReportState(reportid)
        for i in range(1, 5):
            time.sleep(10)
            isGenerated = service.getReportState(reportid)
            print isGenerated

        url = service.getReportFileUrl(reportid)

        printJsonResponse(url)


    except Exception, e:
        print e
        tb.print_exc()




