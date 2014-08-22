package fdd_ads_pipeline;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.base.Joiner;
import com.google.common.collect.Lists;

public class FileUtil {

	private static Logger logger = LoggerFactory.getLogger(FileUtil.class.getCanonicalName());

	private File currentFile;
	
	public static List<String> readLines(String fileName) {
		List<String> lines = Lists.newArrayList();
		try {
			BufferedWriter lineWriter = new BufferedWriter(new FileWriter(new File(fileName)));
		} catch (IOException e) {
			e.printStackTrace();
		}
		return lines;
	}
	

	public static void writeLines(String fileName, List<String> lines) {
		// TODO Auto-generated method stub
		return;
	}

	public void createFile(String fileName) {
		currentFile = new File(fileName, "w+");
	}

	public void writeLine(String line) {
		// TODO Auto-generated method stub
		return;
	}

	public void writeCsvLine(List<String> columns) {
		String line = Joiner.on(',').join(columns);
		System.out.println(line);
		for (String value : columns) {
			if (value.contains(",")) {
				logger.warn("ERROR: contains comma in the CSV columms: " + line);
				return;
			}
		}
		writeLine(line);
	}

	public void close() {
	}
}
