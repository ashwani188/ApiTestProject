package com.api.ApiTestProject;

import java.net.MalformedURLException;

import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.AfterSuite;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Parameters;
import org.testng.annotations.Test;

import com.relevantcodes.extentreports.ExtentReports;
import com.relevantcodes.extentreports.ExtentTest;
import com.relevantcodes.extentreports.LogStatus;

public class UiTest {
	WebDriver driver;
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

	@Parameters("browser")
	@BeforeTest
	public void intializeRemoteBrowser(String browserType) throws MalformedURLException {
		driver = BaseClass.intializeRemoteBrowser(browserType);
	}

//	@BeforeMethod
//	public void intializeBrowser(String browserType) {
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
//		BaseClass.intializeBrowser();
//		driver = BaseClass.getDriver();

//	}

	@Test
	public void launchDriver() throws InterruptedException {
//		BaseClass.getDriver().get("https://www.youtube.com");
//		BaseClass.getDriver().manage().deleteAllCookies();

		driver.get("https://www.youtube.com");
		logger = extent.startTest("Launching YOUTUBE");
		CoreUtils.maximizeWin(driver);
		System.out.println("launch youtube");
		System.out.println(Thread.currentThread().getId());
		logger.log(LogStatus.PASS, "Youtube Passed");
	}

	@Test
	public void launchDriver2() {
		driver.get("https://www.facebook.com");
		logger = extent.startTest("Launching  FACEBOOK");
		CoreUtils.maximizeWin(driver);
		System.out.println("launch facebook");
		System.out.println(Thread.currentThread().getId());
		logger.log(LogStatus.PASS, "Facebook Passed");
	}

//	@AfterMethod
//	public void closeBrowser() {
//		BaseClass.closeBrowser();
//	}
	
	@AfterTest
	public void closeRemoteBrowser()
	{
		System.out.println("###############TEST CASES EXECUTION ENDED###############");
		driver.quit();
	}

	@AfterSuite
	public void endReport() {
		extUtils.endReport(logger);
	}

}
