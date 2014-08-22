package fdd_ads_pipeline;

import java.util.Map;
import java.util.Properties;

import com.google.common.collect.Maps;

public class HouseInfoLoader {

	private Map<String, String> houseNameToIdMap = Maps.newHashMap();
	
	public HouseInfoLoader() {
	}
	
	public void init() {
		// Load all info.
		// Fill houseNameToIdMap
	}

	// Return null if not found.
	public String getHouseIdByName(String houseName) {
		return houseNameToIdMap.get(houseName);
	}
}
