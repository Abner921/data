package mongodb.pipeline.config;

import java.util.Map;
import java.util.Properties;

import com.google.common.collect.Maps;

public class ConfigLoader {

	private final Map<String, Properties> propertiesMap = Maps.newHashMap();
	
	public static Properties getJdbcProperties() {
		// TODO: load from txt file
		
		Properties p = new Properties();
		p.setProperty("jdbc.fdd_ads.host", "192.168.9.102");
		p.setProperty("jdbc.fdd_ads.username", "");
		p.setProperty("jdbc.fdd_ads.password", "");
		p.setProperty("jdbc.fdd_ads.port", "27017");
		return p;
	}
}