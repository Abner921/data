#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ErrorCode import *
from FallbackType import *
from MeihuaAdType import *

# UNUSED
MeihuaInitialAction = {
  'action_name': 'MeihuaInitial',
  'headers': {
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Cache-Control': 'max-age=86400',
               'Connection': 'keep-alive',
               'Host': 'adm.meihua.info',
               'Referer': 'http://adm.meihua.info',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36' },
  'result': [{ 'output_key': 'MEIHUA_INITIAL',
               'response_regex' : '(.*)'
            }],
  'error_handling' : [{
    'error_regex' : ".*",
    'error_message' : "Username or password error.",
    'error_code' : ErrorCode.ACTION_LOGIN_ERROR
    }
  ],
  'url': 'http://adm.meihua.info/'
}

# UNUSED
MeihuaInitial2Action = {
  'action_name': 'MeihuaInitial2',
  'headers': {
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Cache-Control': 'max-age=86400',
               'Connection': 'keep-alive',
               'Host': 'adm.meihua.info',
               'Referer': 'http://adm.meihua.info',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36' },
  'result': [{ 'output_key': 'MEIHUA_INITIAL2',
               'response_regex' : '(.*)'
            }],
  'error_handling' : [{
    'error_regex' : ".*",
    'error_message' : "Username or password error.",
    'error_code' : ErrorCode.ACTION_LOGIN_ERROR
    }
  ],
  'url': 'http://adm.meihua.info/actionpage/infoframe.aspx'
}

# Get mhid
MeihuaLogin1Action = {
  'action_name': 'MeihuaLogin1',
  'url_params': { 'rax': '0.9354440867900848',
                  'u': '%==>USERNAME<==%',
                  'p': '%==>PASSWORD<==%'},
  'headers': {
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'adm.meihua.info',
               'Referer': 'http://adm.meihua.info',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36' },
  'result': [{ 'output_key': 'MEIHUA_LOGIN_MHID',
               'response_regex' : 'Set-Cookie: mhid=(.*)'
            }],
  'error_handling' : [{
    'error_regex' : ".*",
    'error_message' : "Username or password error. no mhid.",
    'error_code' : ErrorCode.ACTION_LOGIN_ERROR
    }
  ],
  'url': 'http://adm.meihua.info/actionpage/LoginAjax.aspx'
}

# set login cookie
MeihuaLogin2Action = {
  'action_name': 'MeihuaLogin2',
  'url_params': { 'b' : 'http://adm.meihua.info/actionpage/GetInfo.aspx',
                  'bf': 'http://adm.meihua.info/',
                  'uid': '%==>USERNAME<==%',
                  'md5': 'CYeAgw24Cw9nL6aLGzI/7Q=='},
  'headers': {
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'passport.meihua.info',
               'Referer': 'http://adm.meihua.info',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36' },
  'result': [{ 'output_key': 'MEIHUA_GETINFO_USER',
               'response_regex' : 'USERNAME=USERNAME=(.*)'
            }],
  'error_handling' : [{
    'error_regex' : ".*",
    'error_message' : "Username or password error.",
    'error_code' : ErrorCode.ACTION_LOGIN_ERROR
    }
  ],
  'url': 'http://passport.meihua.info/SetPass.aspx'
}


# UNUSED
MeihuaLogin3Action = {
  'action_name': 'MeihuaLogin3',
  'url_params': { 'bf': 'http://adm.meihua.info/',
                  'uid': '%==>USERNAME<==%',
                  'MD5': 'CYeAgw24Cw9nL6aLGzI/7Q=='},
  'headers': {
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'passport.meihua.info',
               'Referer': 'http://adm.meihua.info',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36' },
  'result': [{ 'output_key': 'MEIHUA_LOGIN3',
               'response_regex' : '(.*)'
            }],
  'error_handling' : [{
    'error_regex' : ".*",
    'error_message' : "Username or password error.",
    'error_code' : ErrorCode.ACTION_LOGIN_ERROR
    }
  ],
  'url': 'http://adm.meihua.info/actionpage/GetInfo.aspx'
}

"""
直接在list内搜索时发出的request，这里会设置cookie标记last search，并且redirect
http://adm.meihua.info/actionpage/QuerySearch.aspx?keyStr=%E4%B8%87%E7%A7%91%20%E4%B8%8A%E6%B5%B7

This action should redirect to listview request:
http://adm.meihua.info/ListView.aspx?adType=0&keyStr=%e4%b8%87%e7%a7%91+%e4%b8%8a%e6%b5%b7


GET /actionpage/QuerySearch.aspx?keyStr=%E4%B8%87%E7%A7%91 HTTP/1.1
Host: adm.meihua.info
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36
Accept-Encoding: gzip,deflate,sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4
Cookie: mhid=hx2rm055zudjub455s1qd3rr; LastSearch_peggy_peng=actionpage%2fQuerySearch.aspx%3fkeyStr%3d%25u4e07%25u79d1%2b%25u4e0a%25u6d77%2c%e4%b8%87%e7%a7%91+%e4%b8%8a%e6%b5%b7@actionpage%2fQuerySearch.aspx%3fkeyStr%3d%25u4e07%25u79d1%2c%e4%b8%87%e7%a7%91; __utma=86614660.1907145492.1403670009.1403746089.1404114585.3; __utmc=86614660; __utmz=86614660.1404114585.3.2.utmcsr=mail.fangdd.com|utmccn=(referral)|utmcmd=referral|utmcct=/cgi-bin/mail_spam; autoLogin=userID=yiling_zhang&passWord=gL22uLq+CSw=&isDES=true; USERNAME=USERNAME=yiling_zhang&MD5=CYeAgw24Cw9nL6aLGzI/7Q==; login=Yes; LastSearch_yiling_zhang=actionpage%2fQuerySearch.aspx%3fkeyStr%3d%25u5730%25u4ea7%2c%e5%9c%b0%e4%ba%a7@actionpage%2fQuerySearch.aspx%3fkeyStr%3d%25u4e07%25u79d1%2c%e4%b8%87%e7%a7%91; ViewType_1=1; ListViewTab=1; _ga=GA1.2.1907145492.1403670009
"""
MeihuaGetSearchCookieAction = {
  'action_name': 'MeihuaGetSearchCookie',
  'url_params': { 'keyStr' : '%==>KEYWORD<==%' },
  'headers': {
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Connection': 'keep-alive',
               'Host': 'adm.meihua.info',
               'Origin': 'http://adm.meihua.info',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'},
  'result': [ { 'output_key': 'MEIHUA_LAST_SEARCH_COOKIE',
                'response_regex': 'LastSearch_(.*)'}],
  'error_handling' : [{
    'error_regex' : ".*",
    'error_message' : "Error when search for keyword.",
    'error_code' : ErrorCode.ACTION_NO_RESULT
    }
  ],
  'url': 'http://adm.meihua.info/actionpage/QuerySearch.aspx'
}

"""
然后再请求对应的结果，获得所有广告的xml
Request URL:http://adm.meihua.info/actionpage/Response.aspx?adType=1&ps=25&st=1&sa=1&sDate=2014-3-25&eDate=2014-6-25&rax=0.9719717337284237
adType:1
ps:25
st:1
sa:1
sDate:2014-3-25
eDate:2014-6-25
rax:0.9354440867900848

response:
<MeihuaNet><Count>8</Count><PageCount>1</PageCount><Last4MonthCount>1145</Last4MonthCount><Item><Repeat>0</Repeat><ID>10073935</ID><HeaderLabel>让更多上海人住进万科装修房</HeaderLabel><AdvertiserID>224821</AdvertiserID><AdvertiserName>昆山万科房地产有限公司</AdvertiserName><BrandCode>254991</BrandCode><BrandName>上海魅力之城</BrandName><BrandNameEN></BrandNameEN><MediumID>419</MediumID><MediumName>I时代报</MediumName><MediumNameEN>METRO EXPRESS</MediumNameEN><CategoryCode>130102</CategoryCode><CategoryName>住宅-公寓</CategoryName><Celebrities></Celebrities><ReleaseDate>2014-06-19</ReleaseDate><PageNumber>第封一版</PageNumber><LayoutStyle>半版</LayoutStyle><PicHeight>11.51</PicHeight><PicWidth>23.09</PicWidth><ProductModel>公寓</ProductModel><AdExpense>4.48</AdExpense><SuppleForceType>硬广告</SuppleForceType><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVoyz0rbAm7b7yCLeC7YU6Hrei0rgejhGsmLqtVT2Ji%2bdd9b9x4wVbHA%3d%3d&amp;fn=picture&amp;t=0</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVoyz0rbAm7b6RkGaWJA36mv93X5tDK7rJwNoCYbKFu38%3d&amp;fn=picture&amp;t=0</GraphicLarge><ColorType>彩色</ColorType><PageSize>0.4</PageSize><PaperType>新闻</PaperType><AdObject>产品宣传</AdObject><MediumCity>上海市</MediumCity><Browse>1】</Browse></Item><Item><Repeat>0</Repeat><ID>10065190</ID><HeaderLabel>万科翡翠别墅掀 拜占庭 风潮</HeaderLabel><AdvertiserID>131563</AdvertiserID><AdvertiserName>上海加来房地产开发有限公司</AdvertiserName><BrandCode>127968</BrandCode><BrandName>上海翡翠别墅</BrandName><BrandNameEN></BrandNameEN><MediumID>318</MediumID><MediumName>东方早报</MediumName><MediumNameEN>ORIENTAL MORNING POST</MediumNameEN><CategoryCode>130103</CategoryCode><CategoryName>住宅-别墅</CategoryName><Celebrities></Celebrities><ReleaseDate>2014-06-19</ReleaseDate><PageNumber>第B16 专题版</PageNumber><LayoutStyle>1/4版</LayoutStyle><PicHeight>16.65</PicHeight><PicWidth>11.68</PicWidth><ProductModel>别墅</ProductModel><AdExpense>4.08</AdExpense><SuppleForceType>软广告</SuppleForceType><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVoyz0rbAm7b6GJ5hTsYfbtCjeiQUmNhQbEUTyIifsqHgmSo9Lso2maA%3d%3d&amp;fn=picture&amp;t=0</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVoyz0rbAm7b7VhJHG9GdDQP1UBahQfDAX%2fD6AQt%2bjjr0%3d&amp;fn=picture&amp;t=0</GraphicLarge><ColorType>彩色</ColorType><PageSize>0.25</PageSize><PaperType>新闻</PaperType><AdObject>产品宣传</AdObject><MediumCity></MediumCity><Browse>1】</Browse></Item><Item><Repeat>0</Repeat><ID>10035604</ID><HeaderLabel>上海万科商用绽放 商办中介誓师大会成功举办</HeaderLabel><AdvertiserID>35970</AdvertiserID><AdvertiserName>万科集团</AdvertiserName><BrandCode>230315</BrandCode><BrandName>万科</BrandName><BrandNameEN></BrandNameEN><MediumID>418</MediumID><MediumName>第一财经日报</MediumName><MediumNameEN>CHINA BUSINESS NEWS</MediumNameEN><CategoryCode>130100</CategoryCode><CategoryName>出租与出售</CategoryName><Celebrities></Celebrities><ReleaseDate>2014-05-30</ReleaseDate><PageNumber>第A15 公司版</PageNumber><LayoutStyle>通栏</LayoutStyle><PicHeight>8.25</PicHeight><PicWidth>33.38</PicWidth><ProductModel>地产商</ProductModel><AdExpense>5.21</AdExpense><SuppleForceType>软广告</SuppleForceType><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVoyz0rbAm7b4L4RpSGJWyhjpWOcsst56Y5gOLcH60RzjXiPLxtuKaGA%3d%3d&amp;fn=picture&amp;t=0</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVoyz0rbAm7b4Ir8ENQHjxIHca%2fktxhbNiMjHIbG4S7jU%3d&amp;fn=picture&amp;t=0</GraphicLarge><ColorType>黑白</ColorType><PageSize>0.17</PageSize><PaperType>轻涂</PaperType><AdObject>企业或品牌形象</AdObject><MediumCity></MediumCity><Browse>1】</Browse></Item><Item><Repeat>0</Repeat><ID>10014250</ID><HeaderLabel>万科广场 上海道 万科金域中央CBD商业中心正式亮相</HeaderLabel><AdvertiserID>166714</AdvertiserID><AdvertiserName>福州市万科房地产有限公司</AdvertiserName><BrandCode>105031</BrandCode><BrandName>福州金域榕郡</BrandName><BrandNameEN></BrandNameEN><MediumID>297</MediumID><MediumName>福州晚报</MediumName><MediumNameEN>FUZHOU EVENING NEWS</MediumNameEN><CategoryCode>130102</CategoryCode><CategoryName>住宅-公寓</CategoryName><Celebrities></Celebrities><ReleaseDate>2014-05-21</ReleaseDate><PageNumber>第A27 今日财富 综合版</PageNumber><LayoutStyle>1/4版</LayoutStyle><PicHeight>8.28</PicHeight><PicWidth>23.98</PicWidth><ProductModel>公寓</ProductModel><AdExpense>1.65</AdExpense><SuppleForceType>软广告</SuppleForceType><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBV91oSuHixNcGX0Yn7bGdYc5ME56J4LpnnK%2f0WRVCW4AR%2fue6aNESNMg%3d%3d&amp;fn=picture&amp;t=0</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBV91oSuHixNcGQ86an5EQkN%2fROMJ%2b%2bXyjW58fNZ%2fnl9wo%3d&amp;fn=picture&amp;t=0</GraphicLarge><ColorType>黑白</ColorType><PageSize>0.25</PageSize><PaperType>新闻</PaperType><AdObject>产品宣传</AdObject><MediumCity>福州市</MediumCity><Browse>1】</Browse></Item><Item><Repeat>0</Repeat><ID>9948627</ID><HeaderLabel>万科城2014载誉归来 城熟体验</HeaderLabel><AdvertiserID>216378</AdvertiserID><AdvertiserName>上海郡科投资管理有限公司</AdvertiserName><BrandCode>266389</BrandCode><BrandName>上海万科城</BrandName><BrandNameEN></BrandNameEN><MediumID>318</MediumID><MediumName>东方早报</MediumName><MediumNameEN>ORIENTAL MORNING POST</MediumNameEN><CategoryCode>130102</CategoryCode><CategoryName>住宅-公寓</CategoryName><Celebrities></Celebrities><ReleaseDate>2014-04-24</ReleaseDate><PageNumber>第B9 广告版</PageNumber><LayoutStyle>整版</LayoutStyle><PicHeight>33.07</PicHeight><PicWidth>24.54</PicWidth><ProductModel>公寓</ProductModel><AdExpense>17.02</AdExpense><SuppleForceType>软广告</SuppleForceType><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVMJmIHFQUfzGxmpMs7vBk7C9Tk%2bjzPmk7z56p0%2fn72nc%3d&amp;fn=picture&amp;t=0</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVMJmIHFQUfzGUk%2bjP%2ba7g8aS4gh0aMjY6JyDQh9YVRJ4%3d&amp;fn=picture&amp;t=0</GraphicLarge><ColorType>彩色</ColorType><PageSize>1.03</PageSize><PaperType>新闻</PaperType><AdObject>产品宣传</AdObject><MediumCity></MediumCity><Browse>1】</Browse></Item><Item><Repeat>0</Repeat><ID>9913343</ID><HeaderLabel>开发商支持不买房 万科新里程闹哪样</HeaderLabel><AdvertiserID>57903</AdvertiserID><AdvertiserName>上海天亿置业发展有限公司</AdvertiserName><BrandCode>267465</BrandCode><BrandName>济南新里程</BrandName><BrandNameEN></BrandNameEN><MediumID>378</MediumID><MediumName>齐鲁晚报</MediumName><MediumNameEN>QILU EVENING NEWS</MediumNameEN><CategoryCode>130102</CategoryCode><CategoryName>住宅-公寓</CategoryName><Celebrities></Celebrities><ReleaseDate>2014-04-02</ReleaseDate><PageNumber>第C03 专版版</PageNumber><LayoutStyle>整版</LayoutStyle><PicHeight>37.29</PicHeight><PicWidth>22.88</PicWidth><ProductModel>公寓</ProductModel><AdExpense>21.45</AdExpense><SuppleForceType>软广告</SuppleForceType><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVMJmIHFQUfzFLdXFHNkx4WaQaPPUMfA8jkiYFlKAXuiQ%3d&amp;fn=picture&amp;t=0</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVMJmIHFQUfzGygAJF0xXbTChwjaeVikkxOg1Wx6XB5Y4%3d&amp;fn=picture&amp;t=0</GraphicLarge><ColorType>彩色</ColorType><PageSize>1</PageSize><PaperType>新闻</PaperType><AdObject>产品宣传</AdObject><MediumCity>济南市</MediumCity><Browse>1】</Browse></Item><Item><Repeat>0</Repeat><ID>9903809</ID><HeaderLabel>百万科鲁兹 百万年轻梦</HeaderLabel><AdvertiserID>67</AdvertiserID><AdvertiserName>上海通用汽车有限公司</AdvertiserName><BrandCode>124593</BrandCode><BrandName>科鲁兹</BrandName><BrandNameEN></BrandNameEN><MediumID>509</MediumID><MediumName>生活报</MediumName><MediumNameEN>LIFE DAILY POST</MediumNameEN><CategoryCode>20508</CategoryCode><CategoryName>轿车/跑车</CategoryName><Celebrities></Celebrities><ReleaseDate>2014-03-25</ReleaseDate><PageNumber>第C20 广告版</PageNumber><LayoutStyle>1/4版</LayoutStyle><PicHeight>16.26</PicHeight><PicWidth>11.52</PicWidth><ProductModel>轿车</ProductModel><AdExpense>3.91</AdExpense><SuppleForceType>硬广告</SuppleForceType><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVMJmIHFQUfzHKbzcPBsGx7DDj%2f3%2fNlIWtr2BSzoyQaXs%3d&amp;fn=picture&amp;t=0</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVMJmIHFQUfzFcHP8YMCslx1hbKDvuTSdspgG3mznRJHo%3d&amp;fn=picture&amp;t=0</GraphicLarge><ColorType>彩色</ColorType><PageSize>0.24</PageSize><PaperType>新闻</PaperType><AdObject>产品宣传</AdObject><MediumCity>哈尔滨市</MediumCity><Browse>1】</Browse></Item><Item><Repeat>0</Repeat><ID>9851907</ID><HeaderLabel>让上海一部分青年先住起来</HeaderLabel><AdvertiserID>224821</AdvertiserID><AdvertiserName>昆山万科房地产有限公司</AdvertiserName><BrandCode>255534</BrandCode><BrandName>昆山万科MIXTOWN</BrandName><BrandNameEN></BrandNameEN><MediumID>419</MediumID><MediumName>I时代报</MediumName><MediumNameEN>METRO EXPRESS</MediumNameEN><CategoryCode>130102</CategoryCode><CategoryName>住宅-公寓</CategoryName><Celebrities></Celebrities><ReleaseDate>2014-03-06</ReleaseDate><PageNumber>第特4 轨道地产版</PageNumber><LayoutStyle>半版</LayoutStyle><PicHeight>14.27</PicHeight><PicWidth>23.29</PicWidth><ProductModel>公寓</ProductModel><AdExpense>5.61</AdExpense><SuppleForceType>硬广告</SuppleForceType><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBV%2bsxj6kRCxl7Q45KZoSc6Uuq6H3WawrZrTWavirRlofs%3d&amp;fn=picture&amp;t=0</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=0&amp;p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBV%2bsxj6kRCxl4Mt6SHkjqXXIV7P6UMJWHWiDIaXMjoRlQ%3d&amp;fn=picture&amp;t=0</GraphicLarge><ColorType>彩色</ColorType><PageSize>0.5</PageSize><PaperType>新闻</PaperType><AdObject>产品宣传</AdObject><MediumCity>上海市</MediumCity><Browse>1】</Browse></Item><EnumList><BrandList><BrandItem ID="105031">福州金域榕郡</BrandItem><BrandItem ID="267465">济南新里程</BrandItem><BrandItem ID="124593">科鲁兹</BrandItem><BrandItem ID="255534">昆山万科MIXTOWN</BrandItem><BrandItem ID="127968">上海翡翠别墅</BrandItem><BrandItem ID="254991">上海魅力之城</BrandItem><BrandItem ID="266389">上海万科城</BrandItem><BrandItem ID="230315">万科</BrandItem></BrandList><GeoList><GeoItem Name="上海市" ID="9"><Medium ID="419">I时代报</Medium><Medium ID="318">东方早报</Medium><Medium ID="418">第一财经日报</Medium></GeoItem><GeoItem Name="福建省" ID="13"><CityList><CityItem Name="福州市"><Medium ID="297">福州晚报</Medium></CityItem></CityList></GeoItem><GeoItem Name="山东省" ID="15"><CityList><CityItem Name="济南市"><Medium ID="378">齐鲁晚报</Medium></CityItem></CityList></GeoItem><GeoItem Name="黑龙江省" ID="8"><CityList><CityItem Name="哈尔滨市"><Medium ID="509">生活报</Medium></CityItem></CityList></GeoItem></GeoList><LStyleList><LStyleItem ID="-2">报纸</LStyleItem><LStyleItem ID="100"> --整版</LStyleItem><LStyleItem ID="101"> --半版</LStyleItem><LStyleItem ID="102"> --通栏</LStyleItem><LStyleItem ID="103"> --1/4版</LStyleItem><LStyleItem ID="104"> --1/4直版</LStyleItem><LStyleItem ID="105"> --报眼</LStyleItem><LStyleItem ID="106"> --半页跨版</LStyleItem><LStyleItem ID="107"> --整页跨版</LStyleItem><LStyleItem ID="108"> --1/3版</LStyleItem><LStyleItem ID="109"> --半通栏</LStyleItem><LStyleItem ID="111"> --其他</LStyleItem><LStyleItem ID="112"> --报眉</LStyleItem><LStyleItem ID="-3">杂志</LStyleItem><LStyleItem ID="200"> --整页</LStyleItem><LStyleItem ID="201"> --半页</LStyleItem><LStyleItem ID="202"> --1/4页</LStyleItem><LStyleItem ID="204"> --通栏</LStyleItem><LStyleItem ID="205"> --跨页(双整版)</LStyleItem><LStyleItem ID="206"> --跨页(双半版)</LStyleItem><LStyleItem ID="208"> --封面封底拉页</LStyleItem><LStyleItem ID="209"> --1/4直版</LStyleItem><LStyleItem ID="210"> --其他</LStyleItem><LStyleItem ID="211"> --蝴蝶拉页</LStyleItem><LStyleItem ID="212"> --1/3页</LStyleItem><LStyleItem ID="213"> --夹带赠品</LStyleItem><LStyleItem ID="214"> --特殊插页</LStyleItem><LStyleItem ID="215"> --1/3页2联</LStyleItem><LStyleItem ID="216"> --1/3页3联</LStyleItem><LStyleItem ID="217"> --1/3页4联</LStyleItem><LStyleItem ID="218"> --1/4页2联</LStyleItem><LStyleItem ID="219"> --1/4页3联</LStyleItem><LStyleItem ID="220"> --1/4页4联</LStyleItem></LStyleList></EnumList><KeySegmentor><![CDATA[万科 上海]]></KeySegmentor></MeihuaNet>

adType:
6: 电台
1: 报刊
2: 电视
3: 户外
4: 网络
5: 促销
"""
MeihuaListAllAction = {
  'action_name': 'MeihuaListAll',
  'url_params': { 'adType': '%==>AD_TYPE<==%',
            'ps': '100',
            'st': '1',
            'sa': '1',
            'sDate': '%==>START_DATE<==%',
            'eDate': '%==>END_DATE<==%',
            'rex': '0.5980183952488005'},
  'headers': { 
               'Accept': '*/*',
               'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Connection': 'keep-alive',
               'Host': 'adm.meihua.info',
               'Content-Type' : 'text/xml',
               'Referer': 'http://adm.meihua.info/ListView.aspx?adType=0&keyStr=%==>KEYWORD<==%',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11'},
  'result': [ { 'output_key': 'MEIHUA_SEARCH_RESULT',
                'result_regex': '<MeihuaNet>(.*?)</MeihuaNet>',
                'match_multiline' : True
              }],
  'error_handling' : [{
    'error_regex' : ".*",
    'error_message' : "No search result found.",
    'error_code' : ErrorCode.ACTION_NO_RESULT
    }
  ],
  'url': 'http://adm.meihua.info/actionpage/Response.aspx'
}

MEIHUA_ACTIONS = [MeihuaLogin1Action, MeihuaLogin2Action, MeihuaLogin3Action,
                  MeihuaGetSearchCookieAction, MeihuaListAllAction]
