package fdd_ads_pipeline;

import java.util.List;
import java.util.Map;

import com.google.common.base.Strings;
import com.google.common.collect.Maps;

public class RegionInfoLoader {


	private Map<String, String> districtNameToIdMap = Maps.newHashMap();
	
	public RegionInfoLoader() {
		init();
	}
	
	public void init() {
		List<String> lines = FileUtil.readLines("district_info.csv");
		for (String line : lines) {
			if(Strings.isNullOrEmpty(line)) {
				continue;
			}
			
			String[] columns = line.split(",");
			String cityId = columns[0];
			String cityName = columns[1];
			String cityFullName = columns[2];
			String cityShortName = columns[3];
			districtNameToIdMap.put(cityName, cityId);
			districtNameToIdMap.put(cityFullName, cityId);
			districtNameToIdMap.put(cityShortName, cityId);
		}
	}
	
	// Return null if not found.
	public String getCityIdByName(String cityName) {
		return districtNameToIdMap.get(cityName);
	}
	
}
