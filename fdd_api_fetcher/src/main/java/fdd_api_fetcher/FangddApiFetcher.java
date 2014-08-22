package fdd_api_fetcher;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fangdd.base.utils.http.HttpClientUtils;
import com.fangdd.base.utils.http.UrlWrapper;
import com.fangdd.base.utils.http.UserAgent;
import com.google.common.collect.Lists;

public class FangddApiFetcher {
	private static Logger logger = LoggerFactory.getLogger(FangddApiFetcher.class.getCanonicalName());
	
	// "house_sale_telephone", "house_households", "house_favorable"
	private static List<String> fieldNames = Lists.newArrayList(
		"house_id", "house_name", "city_id", "city_name", "district_id", "district_name",
		"section_id", "section_name", "house_build_type", "house_property_type", "house_type");

	public static void getAllHouseList() {
		try {
			String url = "http://api.fangdd.com/demo-deal";
			UrlWrapper urlWrapper = new UrlWrapper(url);
			
			Map<String, Object> params = new HashMap<String, Object>();
			params.put("method", "searchHouseList");
			params.put("parameters[fields]", join(fieldNames));
			params.put("parameters[house_name]", "Íò¿Æ");
			urlWrapper.addAllParameter(params);
			
			String json = HttpClientUtils.fetchStringByPost(urlWrapper, UserAgent.FANGDD_SDK_JAVA);
			getHouseValues(json);
		} catch (IOException e) {
			e.printStackTrace();
			throw new RuntimeException("Error when getHouseList http://api.fangdd.com/demo-deal", e);
		}
	}
	
	private static void getHouseValues(String jsonString) {
		try {
			logger.info("JSON: " + jsonString.substring(0, Math.min(200, jsonString.length())));
			JSONObject json= new JSONObject(jsonString);
			JSONArray jsonArray=json.getJSONObject("data").getJSONArray("list");

			System.out.println(join(fieldNames));
			
			for(int i=0;i<jsonArray.length();i++){  
		        JSONObject houseInfo=(JSONObject) jsonArray.get(i);
		        
				List<String> fields = new ArrayList<String>();
		        for (String field : fieldNames) {
		        	fields.add(houseInfo.getString(field));
		        }
		        System.out.println(join(fields));
		    }
		} catch (Exception e) {
			e.printStackTrace();
		}
		return;
	}
	
	private static String join(List<String> values) {
		String val = "";
		for (String v : values) {
			if (val.isEmpty()) {
				val = v;
			} else {
				val += (","  + v);
			}
		}
		return val;
	}
	
	public  static void main(String[] args){
		getAllHouseList();
	}
}

