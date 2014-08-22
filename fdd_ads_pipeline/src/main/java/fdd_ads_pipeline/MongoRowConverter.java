package fdd_ads_pipeline;

import com.mongodb.DBObject;

public interface MongoRowConverter {
	DBObject convert(DBObject raw);
}
