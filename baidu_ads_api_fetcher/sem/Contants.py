#encoding=utf-8

class Contants():

    # unitOfTime: 1,3,4,5,7,8 (年报,月报,周报,日报,小旪报,请求旪间段汇总)
    unitOfTimeName={}
    unitOfTimeName[1]= 'year'
    unitOfTimeName[3]= 'month'
    unitOfTimeName[4]= 'week'
    unitOfTimeName[5]= 'day'
    unitOfTimeName[7]= 'hour'
    unitOfTimeName[8]= 'period'

    unitOfTimeId = dict([(value,key) for key,value in unitOfTimeName.items()])

    #device
    deviceName ={}
    deviceName[0] = 'all'
    deviceName[1] = 'pc'
    deviceName[2] = 'mobile'

    deviceId = dict([(value,key) for key,value in deviceName.items()])

    #
if __name__ == "__main__":  #for test
    print Contants.unitOfTime

