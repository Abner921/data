package fdd_ads_pipeline;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ConfigLoader {
	private static Properties jdbcProp;
	
	static {
		String fileName = "jdbc.properties";
		jdbcProp = new Properties();
		try {
			InputStream is = new FileInputStream(FileUtil.getProjectRootPath(fileName));
			jdbcProp.load(is);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static Properties getJdbcProperties() {
		return jdbcProp;
	}
	
}