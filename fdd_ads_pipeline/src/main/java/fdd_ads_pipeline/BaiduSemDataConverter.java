package fdd_ads_pipeline;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.base.Strings;
import com.google.common.collect.ImmutableMap;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class BaiduSemDataConverter implements MongoRowConverter {
	private static Logger logger = LoggerFactory.getLogger(SemDataProcessor.class.getCanonicalName());
	
	/*
	private static String testData = {
	    "_id" : ObjectId("53fb148b155363827d35ce72"),
	    "account" : "baidu-房多多-上海8131931",
	    "accountId" : "7034363",
	    "adgroupId" : "536529173",
	    "adgroupName" : "城市品牌词",
	    "campaignId" : "16690006",
	    "campaignName" : "昆明-实力壹方城-全国",
	    "click" : "0",
	    "cost" : "0.00",
	    "cpc" : "0.00",
	    "createDate" : "2014-08-25 10:56:38",
	    "date" : "2014-08-24",
	    "deviceId" : 1,
	    "deviceName" : "pc",
	    "impression" : "1",
	    "keyword" : "昆明实力壹方城样板房",
	    "keywordId" : "8726364805",
	    "reportType" : "Keyword",
	    "unitOfTimeId" : 5,
	    "unitOfTimeName" : "day",
	    "wordId" : "1473272222"
	};
	
	// region
	{
    "_id" : ObjectId("53f74e16155363827d35ba35"),
    "account" : "baidu-房多多-上海8131931",
    "accountId" : "7034363",
    "adgroupId" : "536090603",
    "adgroupName" : "城市竞品词",
    "campaignId" : "16792143",
    "campaignName" : "昆明-东盟森林-全国",
    "click" : "0",
    "cost" : "0.00",
    "cpc" : "0.00",
    "createDate" : "2014-08-22 14:05:07",
    "date" : "2014-08-21",
    "deviceId" : 1,
    "deviceName" : "pc",
    "impression" : "13",
    "region" : "北京",
    "regionId" : "1000",
    "reportType" : "Region",
    "unitOfTimeId" : 5,
    "unitOfTimeName" : "day"
    }
	*/
	
	private static Map<String, String> BAIDU_SEM_COLUMN_NAME_MAP = ImmutableMap.<String, String>builder()
			.put("impression", "impression")
			.put("date", "date")
			.put("click", "click")
			.put("cost", "cost")
			.put("keywordId", "keyword_id")
			.put("wordId", "word_id")
			.put("keyword", "keyword_name")
			.put("accountId", "account_id")
			.put("account", "account_name")
			.put("campaignId", "campaign_id")
			.put("campaignName", "campaign_name")
			.put("deviceName", "device")
			.put("adgroupName", "adgroup_name")
			.put("adgroupId", "adgroup_id")
			.build();
	
	/*
	"house_id" : "123",
    "house_name" : "实力壹方城",
    "house_city_id" : 234,
    "keyword_type" : "品牌词",
    "serving_type" : "全国",
    "serving_region" : "北京"
	*/
	
	@Override
	public DBObject convert(DBObject raw) {
		logger.info("Baidu SEM raw: " + raw.toString());
		
		String campaignName = raw.get("campaignName").toString();
		String houseName = getHouseNameFromCampaignName(campaignName);
		String servingType = getServingTypeFromCampaignName(campaignName);
		String servingRegion = getServingRegionFromCampaignName(campaignName);
		String houseId = getHouseIdByName(houseName);
		String houseCityId = getHouseCityId(houseId);
		
		DBObject semRow = new BasicDBObject();
		for (String originColumn : BAIDU_SEM_COLUMN_NAME_MAP.keySet()) {
			Object value = raw.get(originColumn);
			// avoid value.toString throw NullPointerException
			value = (value==null) ? "" : value;
			semRow.put(BAIDU_SEM_COLUMN_NAME_MAP.get(originColumn), value.toString());
		}

		semRow.put("type", "baidu_sem");
		semRow.put("house_id", houseId);
		semRow.put("house_name", houseName);
		semRow.put("house_city_id", houseCityId);
		semRow.put("keyword_type", "");
		semRow.put("serving_type", servingType);
		semRow.put("serving_region", servingRegion);
		
		return semRow;
	}

	private String getHouseCityId(String houseName) {
		return HouseInfoLoader.getHouseIdByName(houseName);
	}

	private String getHouseIdByName(String houseName) {
		return HouseInfoLoader.getHouseIdByName(houseName);
	}

	private String getHouseNameFromCampaignName(String campaignName) {
		if(!Strings.isNullOrEmpty(campaignName)) {
			return campaignName.split("-")[1];
		}
		return null;
	}
	
	private String getServingRegionFromCampaignName(String campaignName) {
		if(!Strings.isNullOrEmpty(campaignName)) {
			return campaignName.split("-")[0];
		}
		return null;
	}

	private String getServingTypeFromCampaignName(String campaignName) {
		if(!Strings.isNullOrEmpty(campaignName)) {
			return campaignName.split("-")[2];
		}
		return null;
	}
}
