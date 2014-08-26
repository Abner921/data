package fdd_ads_pipeline;

import java.util.List;
import java.util.Map;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Maps;

public class HouseInfoLoader {

	private static Map<String, String> houseNameToIdMap = Maps.newHashMap();
	private static Map<String, String> houseNameToCityIdMap = Maps.newHashMap();
	
	static {
		List<Map<String, String>> houseList = FangddApiFetcher.getAllHouseList(
				ImmutableList.of(
						FangddApiFetcher.HOUSE_NAME, FangddApiFetcher.HOUSE_ID,
						FangddApiFetcher.HOUSE_CITY_ID));

		// Fill houseNameToIdMap
		for (Map<String, String> houseInfo : houseList) {
			houseNameToIdMap.put(
					houseInfo.get(FangddApiFetcher.HOUSE_NAME),
					houseInfo.get(FangddApiFetcher.HOUSE_ID));
			houseNameToCityIdMap.put(
					houseInfo.get(FangddApiFetcher.HOUSE_NAME),
					houseInfo.get(FangddApiFetcher.HOUSE_CITY_ID));
		}
	}

	private HouseInfoLoader() {
		// ensure the config info to load only once
	}

	public static String getHouseIdByName(String houseName) {
		return houseNameToIdMap.get(houseName);
	}

	public static String getHouseCityIdByName(String houseName) {
		return houseNameToCityIdMap.get(houseName);
	}
}
