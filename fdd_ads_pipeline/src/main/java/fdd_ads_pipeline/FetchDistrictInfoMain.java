package fdd_ads_pipeline;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Properties;

import com.google.common.collect.Lists;

// Fetching the district info and save into csv.
public class FetchDistrictInfoMain {

	public static void main(String[] args) throws SQLException {
		MySqlLayer mysql = new MySqlLayer();
		
		Properties prop = ConfigLoader.getJdbcProperties();
		String driverName = (String) prop.get("jdbc.driver");
		String serverUrl = (String) prop.get("jdbc.fdd_basic.url");
		String userName = (String) prop.get("jdbc.fdd_basic.username");
		String password = (String) prop.get("jdbc.fdd_basic.password");
		mysql.Connect(driverName, serverUrl, userName, password);
		ResultSet allDistricts = mysql.query(
				"select district_id, district_name, district_full_name, district_short_name from fdd_basic.t_districts;");
		
		String fileName = "";
		FileUtil fileUtil = new FileUtil();
		fileUtil.createFile(fileName);
		while (allDistricts.next()) {
			fileUtil.writeCsvLine(Lists.newArrayList(
					allDistricts.getString(1),
					allDistricts.getString(2),
					allDistricts.getString(3),
					allDistricts.getString(4)));
		}
		fileUtil.close();
		
		mysql.close();
	}

}
