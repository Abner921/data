package fdd_ads_pipeline;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fangdd.base.utils.http.HttpClientUtils;
import com.fangdd.base.utils.http.UrlWrapper;
import com.fangdd.base.utils.http.UserAgent;
import com.google.common.base.Joiner;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Lists;
import com.google.common.collect.Maps;

public class FangddApiFetcher {
	private static Logger logger = LoggerFactory.getLogger(FangddApiFetcher.class.getCanonicalName());

	public static String HOUSE_NAME = "house_name";
	public static String HOUSE_ID = "house_id";
	public static String HOUSE_PROPERTY_TYPE = "house_property_type";
	public static String HOUSE_TYPE = "house_type";
	public static String HOUSE_BUILD_TYPE = "house_build_type";
	public static String HOUSE_CITY_NAME = "city_name";
	public static String HOUSE_CITY_ID = "city_id";
	public static String DISTRICT_NAME = "district_name";
	public static String DISTRICT_ID = "district_id";
	public static String SECTION_NAME = "section_name";
	public static String SECTION_ID = "section_id";
	
	public static String callApi(
			String method, List<String> fieldNames, Map<String, String> parameters) {
		try {
			String url = "http://api.fangdd.com/demo-deal";
			UrlWrapper urlWrapper = new UrlWrapper(url);

			Map<String, Object> params = new HashMap<String, Object>();
			params.put("method", method);
			params.put("parameters[fields]", Joiner.on(",").join(fieldNames));
			for (String matchField : parameters.keySet()) {
				params.put("parameters[" + matchField + "]", parameters.get(matchField));
			}
			urlWrapper.addAllParameter(params);
			
			return HttpClientUtils.fetchStringByPost(urlWrapper, UserAgent.FANGDD_SDK_JAVA);
		} catch (IOException e) {
			e.printStackTrace();
			throw new RuntimeException("Error when getHouseList http://api.fangdd.com/demo-deal", e);
		}
	}

	private static List<JSONObject> parseJsonList(String jsonString) {
		List<JSONObject> results = Lists.newArrayList();
		try {
			logger.info("JSON: " + jsonString.substring(0, Math.min(200, jsonString.length())));
			JSONObject json = new JSONObject(jsonString);
			JSONArray jsonArray = json.getJSONObject("data").getJSONArray("list");

			for(int i=0;i<jsonArray.length();i++){  
		        JSONObject jsonObj = (JSONObject) jsonArray.get(i);
		        if (jsonObj == null) {
		        	continue;
		        }
		        results.add(jsonObj);
		    }
		} catch (JSONException e) {
			e.printStackTrace();
		}
		return results;
	}

	private static List<Map<String, String>> getHouseValues(String jsonString, List<String> fieldNames) {
		List<Map<String, String>> results = Lists.newArrayList();
		for (JSONObject houseInfo : parseJsonList(jsonString)) {
			Map<String, String> fields = Maps.newHashMap();
	        for (String field : fieldNames) {
	        	try {
					fields.put(field, houseInfo.getString(field));
				} catch (JSONException e) {
					logger.error("No field " + field + " for json object: " + houseInfo.toString());
				}
	        }
	        results.add(fields);
		}
		return results;
	}

	
	/*
	 * "house_id":"75",
	 * "house_logo":"http:\/\/fs.fangdd.com\/image\/000\/000\/131\/j2DAJNhcwCl9DS8MlzI5iSUXkaA.jpg",
	 * "house_name":"\u4e07\u79d1\u957f\u98ce\u522b\u5885",
	 * "house_address":" \u5e72\u5c06\u8def\u4e0e\u4e1c\u73af\u8def\u4ea4\u53c9\u5904(\u82cf\u5927\u4e1c\u6821\u533a\u5317)",
	 * "house_sale_telephone":"0512-67581111",
	 * "house_price":"19000",
	 * "house_build_type":"\u591a\u5c42,\u9ad8\u5c42",
	 * "house_property_type":"\u522b\u5885",
	 * "house_opening_date":"1309449600",
	 * "house_available_date":"1379074320",
	 * "house_households":"276",
	 * "house_decorate_status":"\u6bdb\u576f",
	 * "house_area_build":"48152",
	 * "house_plot_ratio":"1.0",
	 * "house_building_density":"\u226425",
	 * "house_property_limit":null,
	 * "house_developer":"\u82cf\u5dde\u4e2d\u822a\u4e07\u79d1\u957f\u98ce\u7f6e\u4e1a\u6709\u9650\u516c\u53f8\u82cf\u5357\u4e07\u79d1\u7f6e\u4e1a\u6709\u9650\u516c\u53f8",
	 * "house_map_lat":"31.31506656837700000",
	 * "house_map_lng":"120.65395622724000000",
	 * "house_map_zoom":"13",
	 * "house_type":"",
	 * "house_sale_status":"",
	 * "city_id":"3",
	 * "district_id":"26",
	 * "section_id":"36",
	 * "shangquan_id":"0",
	 * "house_favorable":null,
	 * "house_expiration_date":null,
	 * "house_cash_amount":"0",
	 * "house_cash_expiration_date":"0",
	 * "house_tzs_name":"\u82cf\u5dde\u4e2d\u822a\u4e07\u79d1\u957f\u98ce\u7f6e\u4e1a\u6709\u9650\u516c\u53f8",
	 * "house_wy_fees":"4.27",
	 * "house_wy_name":"\u82cf\u5357\u4e07\u79d1\u7269\u4e1a\u7ba1\u7406\u6709\u9650\u516c\u53f8",
	 * "house_area_all":"48713",
	 * "house_parking_digits":null,
	 * "house_basic_parking_digits":"276\u4e2a",
	 * "house_greening_rate":null,
	 * "addtime":"1317372878",
	 * "house_developers_issign":"0",
	 * "house_cash_status":"1",
	 * "house_favorable_status":"1","city_name":"\u82cf\u5dde",
	 * "district_name":null,
	 * "section_name":null,
	 * "shangquan_name":null}],"pages":
	 */
	public static List<Map<String, String>> getAllHouseList(List<String> fieldNames) {
		String json = callApi("getHouseList", fieldNames, ImmutableMap.<String, String>of());
		return getHouseValues(json, fieldNames);
	}
	
	public  static void main(String[] args){
		List<Map<String, String>>  results = getAllHouseList(Lists.newArrayList("house_name", "house_id"));
		for (Map<String, String> value : results) {
			logger.info(value.toString());
		}
	}
}

