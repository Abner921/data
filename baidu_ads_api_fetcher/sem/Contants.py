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

    #account
    account={}

    account['7034363'] = {'username':'baidu-房多多-上海8131931',
                          'password':'Fdt0618',
                          'token':'c66fc7d31b49138be7c54ae4a10e4841',
                          'target':'baidu-房多多-上海8131931'}

    account['7034368'] = {'username':'baidu-房多多-苏州8131931',
                          'password':'Fdt0618',
                          'token':'fdcd22e647be9b78ccde4b8e3a8603fd',
                          'target':'baidu-房多多-苏州8131931'}

    account['7034396'] = {'username':'baidu-房多多-徐州8131931',
                          'password':'Fdt0618',
                          'token':'dab4307943384ce176f9cc31a66b02c8',
                          'target':'baidu-房多多-徐州8131931'}

    account['6840745'] = {'username':'baidu-房多多8131931',
                          'password':'Fdt0618',
                          'token':'6abdca093e9d49f9b9eaa1b78e02f57d',
                          'target':'baidu-房多多8131931'}

    #
if __name__ == "__main__":  #for test
    print Contants.unitOfTime

