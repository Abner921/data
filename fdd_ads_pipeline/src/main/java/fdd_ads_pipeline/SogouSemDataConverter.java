package fdd_ads_pipeline;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.collect.ImmutableMap;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class SogouSemDataConverter implements MongoRowConverter {
	private static Logger logger = LoggerFactory.getLogger(SemDataProcessor.class.getCanonicalName());
	
	private static Map<String, String> SOGOU_SEM_COLUMN_NAME_MAP = ImmutableMap.<String, String>builder()
			.put("推广计划", "campaign_name")
			.put("推广组", "adgroup_name")
			.build();

	@Override
	public DBObject convert(DBObject raw) {
		logger.info("Sogou SEM raw: " + raw.toString());
		
		String campaignName = raw.get("推广计划").toString();
		String houseName = getHouseNameFromCampaignName(campaignName);
		String houseId = getHouseIdByName(houseName);
		String houseCityId = getHouseCityId(houseId);
		
		DBObject semRow = new BasicDBObject();
		for (String originColumn : SOGOU_SEM_COLUMN_NAME_MAP.keySet()) {
			semRow.put(SOGOU_SEM_COLUMN_NAME_MAP.get(originColumn), (String) raw.get(originColumn));
		}
		
		// TODO: add new columns: house / city / others.
		return semRow;
	}

	private String getHouseCityId(String houseId) {
		// TODO Auto-generated method stub
		return null;
	}

	private String getHouseIdByName(String houseName) {
		// TODO Auto-generated method stub
		return null;
	}

	private String getHouseNameFromCampaignName(String campaignName) {
		// TODO Auto-generated method stub
		return null;
	}
}
