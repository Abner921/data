package fdd_ads_pipeline;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.base.Joiner;
import com.google.common.collect.Lists;

public class FileUtil {

	private static Logger logger = LoggerFactory.getLogger(FileUtil.class.getCanonicalName());
	
	public static List<String> readLines(String fileName) {
		File sourceFile = new File(new File("").getAbsolutePath() + File.separator + fileName);
		BufferedReader reader = null;
		List<String> result = Lists.newArrayList();
		try {
			reader = new BufferedReader(new FileReader(sourceFile));
			String line = "";
			while(line != null) {
				line = reader.readLine();
				result.add(line);
			}
		} catch (FileNotFoundException fnfe) {
			fnfe.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				if(reader != null)
					reader.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		
		return result;
	}
	

	public static void writeLines(String fileName, List<String> lines) {
		BufferedWriter writer = null;
		File file = new File(new File("").getAbsolutePath() + File.separator + fileName);
		try {
			writer = new BufferedWriter(new FileWriter(file));
			
			for(String line : lines) {
				writer.write(line);
			}
			writer.flush();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if(writer != null)
					writer.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}


	public void writeCsvLine(String fileName, List<String> columns) {
		String line = Joiner.on(',').join(columns);
		for (String value : columns) {
			if (value.contains(",")) {
				logger.warn("ERROR: contains comma in the CSV columms: " + line);
				return;
			}
		}
		
		File file = new File(new File("").getAbsolutePath() + File.separator + fileName);
		BufferedWriter writer = null;
		try {
			writer = new BufferedWriter(new FileWriter(file, true));
			writer.write(line + '\n');
			writer.flush();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if(writer != null)
					writer.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

}
