package fdd_ads_pipeline;

import java.net.UnknownHostException;
import java.util.Map;
import java.util.Properties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.collect.ImmutableMap;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.Mongo;
import com.mongodb.MongoException;

public class SemDataProcessor {
	private static Logger logger = LoggerFactory.getLogger(SemDataProcessor.class.getCanonicalName());
	
	private static Map<String, String> BAIDU_SEM_COLUMN_NAME_MAP = ImmutableMap.<String, String>builder()
			.put("impression", "impression")
			.put("adgroupId", "adgroup_id")
			.put("keyword", "keyword")
			.build();
	
	public void ProcessBaiduSem() {
		DB rawDB = LoadMongoDb("fdd_ads");
		DBCollection rawCollection = rawDB.getCollection("baidu_sem_raw");
		DBCollection semCollection = rawDB.getCollection("sem_data");
		DBCursor cursor = rawCollection.find();
		
		int i = 0;
		while(cursor.hasNext()) {
			i ++;
			if (i > 100) return;
			
			DBObject row = cursor.next();
			semCollection.insert(ProcessBaiduSemJson(row));
		}
	}

	public DBObject ProcessBaiduSemJson(DBObject raw) {
		logger.info("Baidu SEM raw: " + raw.toString());
		
		String campaignName = raw.get("campaignName").toString();
		String houseName = getHouseNameFromCampaignName(campaignName);
		String houseId = getHouseIdByName(houseName);
		String houseCityId = getHouseCityId(houseId);
		
		DBObject semRow = new BasicDBObject();
		for (String originColumn : BAIDU_SEM_COLUMN_NAME_MAP.keySet()) {
			semRow.put(BAIDU_SEM_COLUMN_NAME_MAP.get(originColumn), (String) raw.get(originColumn));
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

	private DB LoadMongoDb(String datastore) {
		Properties jdbcProp = ConfigLoader.getJdbcProperties();
		String mongoDbHost = jdbcProp.getProperty("jdbc.fdd_ads.host");
		String user = jdbcProp.getProperty("jdbc.fdd_ads.username");
		String pass = jdbcProp.getProperty("jdbc.fdd_ads.password");

        try {
        	Mongo mongo = new Mongo(mongoDbHost);
            DB db = mongo.getDB(datastore);
            // db.authenticate(user, pass);
            return db;
        } catch (UnknownHostException e) {  
            e.printStackTrace();  
        } catch (MongoException e) {
            e.printStackTrace();
        }
        
		return null;
	}
}
