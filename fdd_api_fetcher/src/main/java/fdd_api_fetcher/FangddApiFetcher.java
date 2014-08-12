package fdd_api_fetcher;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;

import com.fangdd.base.utils.http.HttpClientUtils;
import com.fangdd.base.utils.http.UrlWrapper;
import com.fangdd.base.utils.http.UserAgent;

public class FangddApiFetcher {
	private static List<String> fieldNames = new ArrayList<String>();
	
	public static void init() {
		fieldNames.add("house_id");
		fieldNames.add("house_name");
		fieldNames.add("city_id");
		fieldNames.add("city_name");
		fieldNames.add("district_id");
		fieldNames.add("district_name");
		fieldNames.add("section_id");
		fieldNames.add("section_name");
		fieldNames.add("house_build_type");
		fieldNames.add("house_property_type");
		fieldNames.add("house_type");
		/*
		fieldNames.add("house_sale_telephone");
		fieldNames.add("house_households");
		fieldNames.add("house_favorable");
		*/
	}

	public static void getAllHouseList() {
		try {
			String url = "http://api.fangdd.com/demo-deal";
			UrlWrapper urlWrapper = new UrlWrapper(url);
			
			Map<String, Object> params = new HashMap<String, Object>();
			params.put("method", "getHouseList");
			params.put("parameters[fields]", join(fieldNames));
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
			System.out.println("JSON: " + jsonString.substring(0, Math.min(200, jsonString.length())));
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
		init();
		getAllHouseList();
	}
}

