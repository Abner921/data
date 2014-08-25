package fdd_ads_pipeline;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.collect.ImmutableMap;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class BaiduSemDataConverter implements MongoRowConverter {
	private static Logger logger = LoggerFactory.getLogger(SemDataProcessor.class.getCanonicalName());
	
	private static HouseInfoLoader houseInfoLoader = new HouseInfoLoader();

	/*
	private static String testData = {
	    "_id" : ObjectId("53fb148b155363827d35ce72"),
	    "account" : "baidu-�����-�Ϻ�8131931",
	    "accountId" : "7034363",
	    "adgroupId" : "536529173",
	    "adgroupName" : "����Ʒ�ƴ�",
	    "campaignId" : "16690006",
	    "campaignName" : "����-ʵ��Ҽ����-ȫ��",
	    "click" : "0",
	    "cost" : "0.00",
	    "cpc" : "0.00",
	    "createDate" : "2014-08-25 10:56:38",
	    "date" : "2014-08-24",
	    "deviceId" : 1,
	    "deviceName" : "pc",
	    "impression" : "1",
	    "keyword" : "����ʵ��Ҽ�������巿",
	    "keywordId" : "8726364805",
	    "reportType" : "Keyword",
	    "unitOfTimeId" : 5,
	    "unitOfTimeName" : "day",
	    "wordId" : "1473272222"
	};
	
	// region
	{
    "_id" : ObjectId("53f74e16155363827d35ba35"),
    "account" : "baidu-�����-�Ϻ�8131931",
    "accountId" : "7034363",
    "adgroupId" : "536090603",
    "adgroupName" : "���о�Ʒ��",
    "campaignId" : "16792143",
    "campaignName" : "����-����ɭ��-ȫ��",
    "click" : "0",
    "cost" : "0.00",
    "cpc" : "0.00",
    "createDate" : "2014-08-22 14:05:07",
    "date" : "2014-08-21",
    "deviceId" : 1,
    "deviceName" : "pc",
    "impression" : "13",
    "region" : "����",
    "regionId" : "1000",
    "reportType" : "Region",
    "unitOfTimeId" : 5,
    "unitOfTimeName" : "day"
    }
	*/
	
	private static Map<String, String> BAIDU_SEM_COLUMN_NAME_MAP = ImmutableMap.<String, String>builder()
			.put("impression", "impression")
			.put("date", "date")
			.put("impression", "impression")
			.put("click", "click")
			.put("cost", "cost")
			.put("cpc", "cpc")
			.put("keywordId", "keyword_id")
			.put("wordId", "word_id")
			.put("keyword", "keyword_name")
			.put("accountId", "account_id")
			.put("account", "account_name")
			.put("campaignId", "campaign_id")
			.put("campaignName", "campaign_name")
			.put("house_name", "house_name")
			.put("deviceName", "device")
			.put("deviceId", "device_id")
			.put("adgroupName", "adgroup_name")
			.put("adgroupId", "adgroup_id")
			.build();
	
	/*
	"house_id" : "123",
    "house_name" : "ʵ��Ҽ����",
    "house_city_id" : 234,
    "keyword_type" : "Ʒ�ƴ�",
    "serving_type" : "ȫ��",
    "serving_region" : "����"
	*/
	
	@Override
	public DBObject convert(DBObject raw) {
		logger.info("Baidu SEM raw: " + raw.toString());
		
		String campaignName = raw.get("campaignName").toString();
		String houseName = getHouseNameFromCampaignName(campaignName);
		String houseId = getHouseIdByName(houseName);
		String houseCityId = getHouseCityId(houseId);
		
		DBObject semRow = new BasicDBObject();
		for (String originColumn : BAIDU_SEM_COLUMN_NAME_MAP.keySet()) {
			semRow.put(BAIDU_SEM_COLUMN_NAME_MAP.get(originColumn), (String) raw.get(originColumn));
		}

		semRow.put("house_id", houseId);
		semRow.put("house_city_id", houseCityId);
		
		// TODO: add new columns: house / city / others.
		return semRow;
	}

	private String getHouseCityId(String houseName) {
		return houseInfoLoader.getHouseIdByName(houseName);
	}

	private String getHouseIdByName(String houseName) {
		return houseInfoLoader.getHouseIdByName(houseName);
	}

	private String getHouseNameFromCampaignName(String campaignName) {
		// TODO Auto-generated method stub
		return null;
	}
}
