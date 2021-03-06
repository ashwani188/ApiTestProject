package com.api.ApiTestProject;

import org.testng.annotations.AfterMethod;
import org.testng.annotations.AfterSuite;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.Test;

import com.relevantcodes.extentreports.ExtentReports;
import com.relevantcodes.extentreports.ExtentTest;
import com.relevantcodes.extentreports.LogStatus;

public class UiTest {
//	WebDriver driver;
	BaseClass baseObj;
	ExtentUtility extUtils;
	ExtentReports extent;
	ExtentTest logger;

	@BeforeSuite
	public void welcomeUiTest() {
		baseObj = new BaseClass();
		extUtils = new ExtentUtility();
		extent = extUtils.startReport();
	}

	@BeforeMethod
	public void intializeBrowser() {
//		try {
//			driver= BrowserStacBaseClass.intializeBrowser();
//		} catch (InterruptedException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		} catch (ExecutionException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}

//		driver= BaseClass.intializeBrowserStack();
		BaseClass.intializeBrowser();
//		driver = BaseClass.getDriver();

	}

	@Test
	public void launchDriver() throws InterruptedException {
		BaseClass.getDriver().get("https://www.youtube.com");
		logger = extent.startTest("Launching YOUTUBE");
		CoreUtils.maximizeWin(BaseClass.getDriver());
		System.out.println("launch youtube");
		System.out.println(Thread.currentThread().getId());
		logger.log(LogStatus.PASS, "Youtube Passed");
		BaseClass.getDriver().manage().deleteAllCookies();
	}

	@Test
	public void launchDriver2() {
		BaseClass.getDriver().get("https://www.facebook.com");
		logger = extent.startTest("Launching  FACEBOOK");
		CoreUtils.maximizeWin(BaseClass.getDriver());
		System.out.println("launch facebook");
		System.out.println(Thread.currentThread().getId());
		logger.log(LogStatus.PASS, "Facebook Passed");
		BaseClass.getDriver().manage().deleteAllCookies();
	}

	@Test
	public void launchDriver3() {
		BaseClass.getDriver().get("https://www.google.com");
		logger = extent.startTest("Launching GOOGLE");
		CoreUtils.maximizeWin(BaseClass.getDriver());
		System.out.println("launch google");
		System.out.println(Thread.currentThread().getId());
		logger.log(LogStatus.PASS, "Google Passed");
		BaseClass.getDriver().manage().deleteAllCookies();
	}

	@AfterMethod
	public void closeBrowser() {
		BaseClass.closeBrowser();
	}

	@AfterSuite
	public void endReport() {
		extUtils.endReport(logger);
	}

}
