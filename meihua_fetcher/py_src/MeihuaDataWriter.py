#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MeihuaAdType import *
from DatabaseLayer import *

class MeihuaDataWriter:
  
  def isNumberValue(self, key):
    return key.find("ID") >= 0 or key.find("Id") >= 0 or key == "Repeat" or key == "BrandCode"
  
  def getCreateTableSql(self, results, adtype):
    #pprint(result)
    columns = []
    for key in results[0].keys():
      keyName = "`" + key + "`"
      if key.endswith("Time") and key != "VideoTime":
        columns.append(keyName + " date NOT NULL")
      elif self.isNumberValue(key):
        columns.append(keyName + " int")
      elif key.find("Graphic") >= 0 or key.find("Picture") >= 0 or key.find("Url") >= 0 or key.find("Description") >= 0:
        columns.append(keyName + " text")
      else:
        columns.append(keyName + " varchar(255)")
    
    createTableSql = """
    DROP TABLE t_meihua_ad_{{AD_TYPE}};
    CREATE TABLE t_meihua_ad_{{AD_TYPE}} (
        KeywordId int,
        CreationTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        {{OTHER_COLUMNS}}
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8; 
    ALTER TABLE t_meihua_ad_{{AD_TYPE}} ADD PRIMARY KEY ( `ID` ) ;
    """
    createTableSql = createTableSql.replace("{{AD_TYPE}}", MeihuaAdTypeNameMap[adtype])
    createTableSql = createTableSql.replace("{{OTHER_COLUMNS}}", ",\n        ".join(columns))
    return createTableSql
  
  def getCellValueForSql(self, value, key):
    if self.isNumberValue(key):
      if value == "":
        return "-1"
      return value
    
    return value

  def getInsertTableKeyValues(self, keywordId, results, keys):
    keyNames = ['`KeywordId`']
    for key in keys:
      keyNames.append("`" + key + "`")
        
    valueList = []
    # Get the columns and values in the same order.
    for record in results:    
      rows = [str(keywordId)]
      for key in keys:
        if key in record:
          rows.append(self.getCellValueForSql(record[key], key))
        else:
          rows.append(self.getCellValueForSql("", key))
  
      valueList.append(rows)
    return (keyNames, valueList)

  def getInsertTableSql(self, keyNames, adtype):
    # get format like: "(%s, %s, %s ...)"
    sqlFormaterList = []
    for key in keyNames:
      sqlFormaterList.append("%s")
    sqlFormaters = "(" + ", ".join(sqlFormaterList) + ")"

    insertSql = """INSERT INTO t_meihua_ad_{{AD_TYPE}} ({{COLUMN_LIST}}) VALUES
                   {{VALUE_LIST}}"""
    insertSql = insertSql.replace("{{AD_TYPE}}", MeihuaAdTypeNameMap[adtype])
    insertSql = insertSql.replace("{{COLUMN_LIST}}", ", ".join(keyNames))
    insertSql = insertSql.replace("{{VALUE_LIST}}", sqlFormaters)
    return insertSql


  def insertToTable(self, layer, keywordId, results, adtype):
    (keysList, valuesList) = self.getInsertTableKeyValues(keywordId, results, results[0].keys())
    sql = self.getInsertTableSql(keysList, adtype)
    print "===== Inserting: ", sql
    print "===== Values: ", valuesList
    layer.excute(sql, valuesList, True)


"""
if __name__ == "__main__":
  result = '<Count>1</Count><PageCount>1</PageCount><Last4MonthCount>0</Last4MonthCount><Item><Repeat>0</Repeat><ID>4529373</ID><AdvertiserName>中梁地产</AdvertiserName><BrandCode>32626</BrandCode><BrandName>中梁地产</BrandName><BrandNameEN></BrandNameEN><CategoryCode>85|74|218</CategoryCode><CategoryName>房地产类|房地产类|楼盘宣传</CategoryName><ProductID>228288</ProductID><ProductName>中梁香缇公馆</ProductName><Campaign>产品宣传</Campaign><AdTypeID>27</AdTypeID><AdType>长横幅大尺寸广告</AdType><MediaID>279</MediaID><CaptureMedia>温州网</CaptureMedia><Dimension>960×70 像素</Dimension><ChannelID>3969</ChannelID><CapturedChannel>房产</CapturedChannel><Filesize></Filesize><CapturedPageName></CapturedPageName><CaptureTime>2014-03-03</CaptureTime><GraphicSmall>http://adm.meihua.info/PicLoader.aspx?type=1&amp;p=AvDuOM8wJiZ4C698dni3FhA7KopCDEyg0IKPuonx%2bGnlearXvxKiWpHTMIDtJFY1rZCt4c0TRqQ81P%2fXtUwVHPxYTQNj%2fRX%2f&amp;fn=picture&amp;t=1&amp;w=120&amp;h=80</GraphicSmall><GraphicLarge>http://adm.meihua.info/PicLoader.aspx?type=1&amp;p=AvDuOM8wJiZ4C698dni3FhA7KopCDEyg0IKPuonx%2bGnlearXvxKiWpHTMIDtJFY1rZCt4c0TRqQ81P%2fXtUwVHPxYTQNj%2fRX%2f&amp;fn=picture&amp;t=0</GraphicLarge><Browse>1】</Browse></Item><EnumList><BrandList><BrandItem ID="32626">中梁地产</BrandItem></BrandList><EnumIModelList><EnumIModel><IModelID>41</IModelID><IModelName>WAP广告</IModelName></EnumIModel><EnumIModel><IModelID>20</IModelID><IModelName>按钮广告</IModelName></EnumIModel><EnumIModel><IModelID>30</IModelID><IModelName>插播式富媒体广告</IModelName></EnumIModel><EnumIModel><IModelID>27</IModelID><IModelName>长横幅大尺寸广告</IModelName></EnumIModel><EnumIModel><IModelID>28</IModelID><IModelName>长纵式大尺寸广告</IModelName></EnumIModel><EnumIModel><IModelID>24</IModelID><IModelName>弹出窗口广告</IModelName></EnumIModel><EnumIModel><IModelID>22</IModelID><IModelName>对联广告</IModelName></EnumIModel><EnumIModel><IModelID>44</IModelID><IModelName>焦点图</IModelName></EnumIModel><EnumIModel><IModelID>31</IModelID><IModelName>扩展式富媒体广告</IModelName></EnumIModel><EnumIModel><IModelID>42</IModelID><IModelName>栏目赞助</IModelName></EnumIModel><EnumIModel><IModelID>43</IModelID><IModelName>频道合作</IModelName></EnumIModel><EnumIModel><IModelID>40</IModelID><IModelName>其他类型</IModelName></EnumIModel><EnumIModel><IModelID>25</IModelID><IModelName>全屏广告</IModelName></EnumIModel><EnumIModel><IModelID>33</IModelID><IModelName>视频类富媒体广告</IModelName></EnumIModel><EnumIModel><IModelID>36</IModelID><IModelName>视频贴片广告</IModelName></EnumIModel><EnumIModel><IModelID>19</IModelID><IModelName>网幅广告</IModelName></EnumIModel><EnumIModel><IModelID>35</IModelID><IModelName>网络软件广告</IModelName></EnumIModel><EnumIModel><IModelID>46</IModelID><IModelName>微博广告</IModelName></EnumIModel><EnumIModel><IModelID>39</IModelID><IModelName>文字链广告</IModelName></EnumIModel><EnumIModel><IModelID>21</IModelID><IModelName>悬浮广告</IModelName></EnumIModel><EnumIModel><IModelID>26</IModelID><IModelName>正方形大尺寸广告</IModelName></EnumIModel><EnumIModel><IModelID>45</IModelID><IModelName>种子视频</IModelName></EnumIModel></EnumIModelList><AdverList><AdverItem ID="33154">中梁地产</AdverItem></AdverList><EnumMediumList><EnumMediumTypeList><MediumTypeID>23</MediumTypeID><MediumTypeName>地方网站</MediumTypeName><EnumMedia><MediumID>279</MediumID><MediumName>温州网</MediumName></EnumMedia></EnumMediumTypeList></EnumMediumList></EnumList><KeySegmentor><![CDATA[中梁香缇]]></KeySegmentor>'
  from MeihuaDataParser import *
  parser = MeihuaDataParser()
  result = parser.parseData(result)
  writer = MeihuaDataWriter()
  sql, keys = writer.getCreateTableSql(result, "tv")
  writer.getInsertTableSql(result, "tv", keys)
  
"""