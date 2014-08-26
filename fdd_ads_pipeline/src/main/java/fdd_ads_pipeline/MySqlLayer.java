package fdd_ads_pipeline;

import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class MySqlLayer {
	
	private java.sql.Connection connection;

	public boolean Connect(String driverName, String serverUrl, String userName, String password) {
		try {
			Class.forName(driverName);
			connection = DriverManager.getConnection(serverUrl, userName, password);
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}
	
	public void close() {
		try {
			if (connection != null) {
				connection.close();
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public void update(String sql) {
		try {
			PreparedStatement ps = connection.prepareStatement(sql);
			ps.executeUpdate();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	public ResultSet query(String sql) {
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
