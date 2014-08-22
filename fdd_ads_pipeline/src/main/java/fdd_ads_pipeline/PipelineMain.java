package fdd_ads_pipeline;

public class PipelineMain {
	private static SemDataProcessor semProcessor = new SemDataProcessor();
	
	public static void main(String[] args) {
		semProcessor.ProcessBaiduSem();
	}

}
