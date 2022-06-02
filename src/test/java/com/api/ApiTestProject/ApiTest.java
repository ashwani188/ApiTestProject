package com.api.ApiTestProject;

import java.util.Arrays;
import java.util.List;

import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import com.relevantcodes.extentreports.ExtentReports;
import com.relevantcodes.extentreports.ExtentTest;
import com.relevantcodes.extentreports.LogStatus;

import io.restassured.response.Response;

/**
 * Unit test for simple App.
 */
public class ApiTest {
	ApiUtility app;
	String resBody = null;
	ExtentUtility extUtils;
	ExtentReports extent;
	ExtentTest logger;
	ExcelReader getData;

	@BeforeSuite
	public void welcome() {
//		app.show();
		getData = new ExcelReader();
	}

	@DataProvider(name = "data-provider")
	public Object[][] dpMethod() {
		return new Object[][] { { "GET", "https://reqres.in", "/api/users", 1, Arrays.asList(1, 2, 3, 4, 5, 6) },
				{ "GET", "https://reqres.in", "/api/users", 2, Arrays.asList(7, 8, 9, 10, 11, 12) } };
	}

	@DataProvider(name = "data-provider-post")
	public Object[][] dpMethodPost() {
//		return new Object[][] { { "POST", "https://reqres.in", "/api/users", "morpheus" } };
		Object[][] data = getData.readExcel("/src/test/resources/ApiTestData.xlsx", "api_data");
		return data;
	}

	@BeforeTest
	public void startReport() {
		app = new ApiUtility();
		extUtils = new ExtentUtility();
		extent = extUtils.startReport();

	}

	@Test(dataProvider = "data-provider", enabled = true)
	public void getRequest(String reqType, String baseUri, String basePath, int val, List<Integer> expResult) {
		logger = extent.startTest("Get API call", "This is for QueryString: " + val);
		Response actResponse = app.apiRequestWithQueryString(reqType, baseUri, basePath, val, "");
		Assert.assertTrue(app.checkOkResponse(actResponse));
		resBody = app.showBody(actResponse);
		Assert.assertTrue(app.verifyIntegerList(expResult, app.getListKey(resBody)));
		logger.log(LogStatus.PASS, "GET API Test Case Passed");
	}

	@Test(dataProvider = "data-provider-post", enabled = true)
	public void postRequest(String reqType, String baseUri, String basePath, String expResult, String payloadName, String key, String value) {
		logger = extent.startTest("Post API call", "This is for POST API for payload: " + payloadName + " and value: "+ value);
		Response actResponse = app.apiRequestUpdatePayload(reqType, baseUri, basePath, payloadName, key, value);
		Assert.assertTrue(app.checkOkResponse(actResponse));
		resBody = app.showBody(actResponse);
//		Assert.assertEquals(expResult, app.getJsonKey(resBody, "name"));
		logger.log(LogStatus.PASS, "POST API Test Case Passed");
	}

	@AfterMethod
	public void getResult() {
		// endTest(logger) : It ends the current test and prepares to create HTML report
		extent.endTest(logger);
	}

	@AfterTest
	public void endReport() {
		extUtils.endReport(logger);
//		extent.endTest(logger);
//		extent.close();
	}

}
