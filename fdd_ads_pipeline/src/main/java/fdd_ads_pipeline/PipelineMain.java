package fdd_ads_pipeline;

public class PipelineMain {
	public static void main(String[] args) {
		SemDataProcessor semProcessor = new SemDataProcessor();
		semProcessor.ProcessAll();
	}
}
