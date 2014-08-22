package fdd_ads_pipeline;

import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Properties;

public class DB {
	private static java.sql.Connection connection;

	static {
		Properties prop = ConfigLoader.getJdbcProperties();
		String driverName = (String) prop.get("jdbc.driver");
		String serverUrl = (String) prop.get("jdbc.fdd_direct.url");
		String userName = (String) prop.get("jdbc.fdd_direct.username");
		String password = (String) prop.get("jdbc.fdd_direct.password");
		
		try {
			Class.forName(driverName);
			connection = DriverManager.getConnection(serverUrl, userName, password);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void update(String sql) {
		try {
			PreparedStatement ps = connection.prepareStatement(sql);
			ps.executeUpdate();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public static ResultSet query(String sql) {
		PreparedStatement ps = null;
		try {
			ps = connection.prepareStatement(sql);
			return ps.executeQuery();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
	}
	
}
