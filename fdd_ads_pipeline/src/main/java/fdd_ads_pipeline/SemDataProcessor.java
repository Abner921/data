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

	private boolean debug = true;
	
	private BaiduSemDataConverter baiduConverter = new BaiduSemDataConverter();
	private SogouSemDataConverter sogouConverter = new SogouSemDataConverter();
	
	public void ProcessAll() {
		ProcessSem("baidu_sem_raw", baiduConverter);
		ProcessSem("sogou_sem_raw", sogouConverter);
	}
	
	public void ProcessSem(String collectionName, MongoRowConverter converter) {
		DB rawDB = LoadMongoDb("fdd_ads");
		DBCollection rawCollection = rawDB.getCollection(collectionName);
		DBCollection semCollection = rawDB.getCollection("sem_data");
		DBCursor cursor = rawCollection.find();
		
		int i = 0;
		while(cursor.hasNext()) {
			if (debug) {
				i ++;
				if (i > 100) return;				
			}
			DBObject row = cursor.next();
			semCollection.insert(converter.convert(row));
		}
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
