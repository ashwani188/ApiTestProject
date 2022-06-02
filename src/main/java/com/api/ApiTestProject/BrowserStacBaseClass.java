package com.api.ApiTestProject;

import java.net.MalformedURLException;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import java.net.URL;

//Import relevant packages here
public class BrowserStacBaseClass {
	public static final String USERNAME = "ashwanikumar_9I8rxX";
	public static final String SECRATE_KEY = "ap7E9QypmPSy5jizTrvc";
	public static final String URL = "https://" + USERNAME + ":" + SECRATE_KEY + "@hub-cloud.browserstack.com/wd/hub";
	static WebDriver driver = null;

	public static WebDriver intializeBrowser() throws InterruptedException, ExecutionException {
		ExecutorService executorService = Executors.newFixedThreadPool(2); // A pool of 2 threads are being created
																			// here. You can change this as per your
																			// parallel limit
		Set<Callable<String>> callables = new HashSet<Callable<String>>();                        // for each @test two browser will open parallelly in current situation
		callables.add(new Callable<String>() {
			public String call() throws Exception {
				Hashtable<String, String> capsHashtable = new Hashtable<String, String>();
				capsHashtable.put("browser", "safari");
				capsHashtable.put("browser_version", "latest");
				capsHashtable.put("os", "OS X");
				capsHashtable.put("os_version", "Big Sur");
				capsHashtable.put("build", "BStack-[Java] Sample Build");
				capsHashtable.put("name", "Thread 3");
				BrowserStacBaseClass.executeTest(capsHashtable);
				return "Task 3 completed";
			}
		});
		callables.add(new Callable<String>() {
			public String call() throws Exception {
				Hashtable<String, String> capsHashtable = new Hashtable<String, String>();
				capsHashtable.put("browser", "chrome");
				capsHashtable.put("browser_version", "latest");
				capsHashtable.put("os", "Windows");
				capsHashtable.put("os_version", "10");
				capsHashtable.put("build", "BStack-[Java] Sample Build");
				capsHashtable.put("name", "Thread 4");
				BrowserStacBaseClass.executeTest(capsHashtable);
				return "Task 4 completed";
			}
		});
		// You can add as many test functions as Callables as you want
		List<Future<String>> futures;
		futures = executorService.invokeAll(callables);
		for (Future<String> future : futures) {
			System.out.println("future.get = " + future.get());
		}
		executorService.shutdown();
		return driver;
	}

	public static void executeTest(Hashtable<String, String> capsHashtable) {
		String key;
		DesiredCapabilities caps = new DesiredCapabilities();
		// Iterate over the hashtable and set the capabilities
		Set<String> keys = capsHashtable.keySet();
		Iterator<String> keysIterator = keys.iterator();
		while (keysIterator.hasNext()) {
			key = keysIterator.next();
			caps.setCapability(key, capsHashtable.get(key));
		}
		try {
			driver = new RemoteWebDriver(new URL(URL), caps);
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
	}
}
