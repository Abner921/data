package fdd_ads_pipeline;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.base.Strings;
import com.google.common.collect.ImmutableMap;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class SogouSemDataConverter implements MongoRowConverter {
	private static Logger logger = LoggerFactory.getLogger(SemDataProcessor.class.getCanonicalName());
	
	private static Map<String, String> SOGOU_SEM_COLUMN_NAME_MAP = ImmutableMap.<String, String>builder()
			.put("日期", "date")
			.put("展示数", "impression")	
			.put("消耗", "cost")
			.put("点击数", "click")
			.put("推广计划ID", "campaign_id")
			.put("推广计划", "campaign_name")
			.put("推广组ID", "adgroup_id")
			.put("推广组", "adgroup_name")
			.put("关键词id", "keyword_id")
			.put("关键词", "keyword_name")
			.put("账户", "account_name")
			.build();

	@Override
	public DBObject convert(DBObject raw) {
		logger.info("Sogou SEM raw: " + raw.toString());
		
		String campaignName = raw.get("推广计划").toString();
		String houseName = getHouseNameFromCampaignName(campaignName);
		String serveRegion = getServeRegionFromCampaignName(campaignName);
		String device = getDeviceFromCampaignName(campaignName);
		String houseId = getHouseIdByName(houseName);
		String houseCityId = getHouseCityId(houseId);
		
		String campaignGroup = raw.get("推广组").toString();
		String keywordType = getKeywordTypeFromCampaignGroup(campaignGroup);
		
		DBObject semRow = new BasicDBObject();
		for (String originColumn : SOGOU_SEM_COLUMN_NAME_MAP.keySet()) {
			Object value = raw.get(originColumn);
			// avoid value.toString throw NullPointerException
			value = (value==null) ? "" : value;
			semRow.put(SOGOU_SEM_COLUMN_NAME_MAP.get(originColumn), value.toString());
		}
		
		semRow.put("type", "sogou_sem");
		semRow.put("device", device);
		semRow.put("house_id", houseId);
		semRow.put("house_name", houseName);
		semRow.put("house_city_id", houseCityId);
		semRow.put("keyword_type", keywordType);
		semRow.put("serving_type", "");
		semRow.put("serving_region", serveRegion);
		
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
			return campaignName.split("-")[2];
		}
		return null;
	}
	
	private String getServeRegionFromCampaignName(String campaignName) {
		if(!Strings.isNullOrEmpty(campaignName)) {
			return campaignName.split("-")[1];
		}
		return null;
	}
	
	private String getDeviceFromCampaignName(String campaignName) {
		if(!Strings.isNullOrEmpty(campaignName)) {
			return campaignName.split("-")[0];
		}
		return null;
	}
	
	private String getKeywordTypeFromCampaignGroup(String campaignGroup) {
		if(!Strings.isNullOrEmpty(campaignGroup)) {
			return campaignGroup.split("-")[0];
		}
		return null;
	}
}
