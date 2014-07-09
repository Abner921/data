#!/usr/bin/env python
# coding=utf-8

import os,sys,time
from xml.dom import minidom

"""
<MeihuaNet>
<Count>8</Count>
<PageCount>1</PageCount>
<Last4MonthCount>1145</Last4MonthCount>
<Item>
<Repeat>0</Repeat>
<ID>10073935</ID>
<HeaderLabel>让更多上海人住进万科装修房</HeaderLabel>
<AdvertiserID>224821</AdvertiserID>
<AdvertiserName>昆山万科房地产有限公司</AdvertiserName>
<BrandCode>254991</BrandCode>
<BrandName>上海魅力之城</BrandName>
<BrandNameEN/>
<MediumID>419</MediumID>
<MediumName>I时代报</MediumName>
<MediumNameEN>METRO EXPRESS</MediumNameEN>
<CategoryCode>130102</CategoryCode>
<CategoryName>住宅-公寓</CategoryName>
<Celebrities/>
<ReleaseDate>2014-06-19</ReleaseDate>
<PageNumber>第封一版</PageNumber>
<LayoutStyle>半版</LayoutStyle>
<PicHeight>11.51</PicHeight>
<PicWidth>23.09</PicWidth>
<ProductModel>公寓</ProductModel>
<AdExpense>4.48</AdExpense>
<SuppleForceType>硬广告</SuppleForceType>
<GraphicSmall>
http://adm.meihua.info/PicLoader.aspx?type=0&p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVoyz0rbAm7b7yCLeC7YU6Hrei0rgejhGsmLqtVT2Ji%2bdd9b9x4wVbHA%3d%3d&fn=picture&t=0
</GraphicSmall>
<GraphicLarge>
http://adm.meihua.info/PicLoader.aspx?type=0&p=sBoehHjcSW6FUxXzUcThFgx6V7rXvsBVoyz0rbAm7b6RkGaWJA36mv93X5tDK7rJwNoCYbKFu38%3d&fn=picture&t=0
</GraphicLarge>
<ColorType>彩色</ColorType>
<PageSize>0.4</PageSize>
<PaperType>新闻</PaperType>
<AdObject>产品宣传</AdObject>
<MediumCity>上海市</MediumCity>
<Browse>1】</Browse>
</Item>
"""

class MeihuaDataParser:

  def parseData(self, xml_content):
    all_items = []
    dom = minidom.parseString("<root>" + xml_content + "</root>")
    for node in dom.getElementsByTagName('Item'):
      # get all key value pair
      one_item = {}
      # for each child there should be only one sub text child.
      for child in node.childNodes:
        if (len(child.childNodes) > 0):
          subchild = child.childNodes[0]
          text = subchild.nodeValue
          one_item[child.nodeName] = text          
      all_items.append(one_item)

    return all_items
  
  