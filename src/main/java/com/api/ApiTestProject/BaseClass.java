package com.api.ApiTestProject;

import java.net.MalformedURLException;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Set;
import java.net.URL;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.remote.BrowserType;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;

import com.beust.jcommander.Parameter;

import io.github.bonigarcia.wdm.WebDriverManager;

public class BaseClass {
	public static Logger logger = null;
	static WebDriver driverStack = null;
	public static final String USERNAME = "ashwanikumar_9I8rxX";
	public static final String SECRATE_KEY = "ap7E9QypmPSy5jizTrvc";
	public static final String URL = "https://" + USERNAME + ":" + SECRATE_KEY + "@hub-cloud.browserstack.com/wd/hub";
	private static ThreadLocal<WebDriver> driver = new ThreadLocal<WebDriver>();

	public BaseClass() {
		String log4jpath = System.getProperty("user.dir") + "/src/main/resources/log4j.properties";
		PropertyConfigurator.configure(log4jpath);
		logger = Logger.getLogger(BaseClass.class);
	}

	public static void executetest1(Hashtable<String, String> capsHashTable) {
		String key;
		DesiredCapabilities caps = new DesiredCapabilities();
		Set<String> keys = capsHashTable.keySet();
		Iterator<String> itr = keys.iterator();
		while (itr.hasNext()) {
			key = itr.next();
			caps.setCapability(key, capsHashTable.get(key));
		}
		try {
			driverStack = new RemoteWebDriver(new URL(URL), caps);

		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
	}

	public static WebDriver intializeBrowserStack() {
//		String build_name = System.getenv("BROWSERSTACK_BUILD_NAME");   //use during jenkins execution
		Hashtable<String, String> capsHashTable = new Hashtable<String, String>();
		capsHashTable.put("browser", "chrome");
		capsHashTable.put("browser_version", "96.0");
		capsHashTable.put("os", "Windows");
		capsHashTable.put("os_version", "10");
//		capsHashTable.put("build_name", build_name);
		capsHashTable.put("name", "Thread1_UIcase");
		BaseClass.executetest1(capsHashTable);
		return driverStack;

	}

	public static void intializeBrowser() {
		logger.info("----------------------Initializing Chrome Browser----------------------");
		WebDriverManager.chromedriver().setup();
		driver.set(new ChromeDriver());
	}

	public static WebDriver getDriver() {
		return driver.get();
	}

	public static void closeBrowser() {
		driver.get().close();
		driver.remove();
		logger.info("----------------------Closed Chrome Browser----------------------");
	}

	public static void intializeRemoteBrowser(String browserType) throws MalformedURLException {
		DesiredCapabilities cap = new DesiredCapabilities();
		if (browserType.equalsIgnoreCase("chrome")) {
			cap.setBrowserName(BrowserType.CHROME);
			WebDriverManager.chromiumdriver().setup();
			System.out.println("########### TEST CASE EXECUTION STARTED ON ==>" + browserType);
		}

		else if (browserType.equalsIgnoreCase("firefox")) {
			cap.setBrowserName(BrowserType.FIREFOX);
			WebDriverManager.firefoxdriver().setup();
			System.out.println("########### TEST CASE EXECUTION STARTED ON ==>" + browserType);
		}

		driver.set(new RemoteWebDriver(new URL("http://localhost:4444/wd/hub"), cap));
	}

}
