package com.api.ApiTestProject;

import java.io.File;

import com.relevantcodes.extentreports.ExtentReports;
import com.relevantcodes.extentreports.ExtentTest;

public class ExtentUtility {
	ExtentReports extent;

	public ExtentUtility() {
		extent = new ExtentReports(System.getProperty("user.dir") + "/test-output/STMExtentReport.html", true);
	}

	public ExtentReports startReport() {

		extent.addSystemInfo("Host Name", "SoftwareTesting").addSystemInfo("Environment", "Automation Testing")
				.addSystemInfo("User Name", "Ashwani Kumar");
		extent.loadConfig(new File(System.getProperty("user.dir") + "/src/main/resources/extent-config.xml"));
		return extent;
	}

	public void endReport(ExtentTest log) {
		extent.endTest(log);
		extent.flush();
//		extent.close();
	}

}
