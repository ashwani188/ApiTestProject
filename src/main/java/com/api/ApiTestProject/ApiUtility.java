package com.api.ApiTestProject;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.*;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.simple.parser.JSONParser;

import io.restassured.RestAssured;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

/**
 * Hello world!
 *
 */
public class ApiUtility extends BaseClass

{
	Response res;
	RequestSpecBuilder builder;
	RequestSpecification rspec;
	JSONParser parser = null;
	JSONObject json = null;
	JSONArray arr = null;
	JSONObject updatedPayload;
	String payload;
	JSONObject jsonPayload;

	public ApiUtility() {
		String log4jpath = System.getProperty("user.dir") + "/src/main/resources/log4j.properties";
		PropertyConfigurator.configure(log4jpath);
		logger = Logger.getLogger(ApiUtility.class);
		parser = new JSONParser();
	}

	public Response apiRequestWithQueryString(String reqType, String baseUri, String basePath, int queryVal,
			String payloadName) {
		builder = new RequestSpecBuilder();
		if (reqType.equals("GET")) {
			builder.setBaseUri(baseUri);
			builder.setBasePath(basePath);
			builder.addQueryParam("page", queryVal);
			rspec = builder.build();
			res = RestAssured.given().spec(rspec).get();
		} else if (reqType.equals("POST")) {
			try {
				payload = new String(Files.readAllBytes(Paths
						.get(System.getProperty("user.dir") + "/src/main/resources/payload/" + payloadName + ".json")));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			builder.setBaseUri("https://reqres.in/");
			builder.setBasePath("/api/users");
			builder.setBody(payload);
			rspec = builder.build();
			res = RestAssured.given().spec(rspec).post();
		}
		return res;

	}

	public Response apiRequestWithoutQueryString(String reqType, String baseUri, String basePath, String payloadName) {
		builder = new RequestSpecBuilder();
		if (reqType.equals("GET")) {
			builder.setBaseUri("http://restapi.adequateshop.com/");
			builder.setBasePath("/api/Tourist");
			rspec = builder.build();
			res = RestAssured.given().spec(rspec).get();
		} else if (reqType.equals("POST")) {
			try {
				payload = new String(Files.readAllBytes(Paths
						.get(System.getProperty("user.dir") + "/src/main/resources/payload/" + payloadName + ".json")));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			builder.setBaseUri(baseUri);
			builder.setBasePath(basePath);
			builder.setBody(payload);
			rspec = builder.build();
			res = RestAssured.given().spec(rspec).post();
		}
		return res;

	}

	public boolean checkOkResponse(Response response) {
		if (response.getStatusCode() == 200) {
			logger.info("---------" + response.statusCode() + "---------------");
			logger.info("get API passed");
			return true;
		} else if (response.getStatusCode() == 201) {
			logger.info("---------" + response.statusCode() + "---------------");
			logger.info("post API passed");
			return true;
		}
		return false;

	}

	public String showBody(Response resBody) {
		String resposeBody = resBody.getBody().asString();
		logger.info(resposeBody);
		return resposeBody;
	}

	public List<Integer> getListKey(String res) {
		List<Integer> a = new ArrayList<Integer>();
		json = new JSONObject(res);
		arr = json.getJSONArray("data");
		for (int i = 0; i < arr.length(); i++) {
			a.add(arr.getJSONObject(i).getInt("id"));
		}
		System.out.println("List of element: " + a);

		return a;
	}

	public String getJsonKey(String res, String key) {
		json = new JSONObject(res);
		return (String) json.get(key);
	}

	public boolean verifyIntegerList(List<Integer> expected, List<Integer> actual) {
		boolean flag = false;
		for (int i = 0; i < actual.size(); i++) {
			System.out.println("expected : " + expected.get(i) + "Actual " + actual.get(i));
			if (expected.get(i).equals(actual.get(i))) {
				flag = true;
			}
		}
		return flag;
	}

	public Response apiRequestUpdatePayload(String reqType, String baseUri, String basePath, String payloadName,
			String key, String value) {
		builder = new RequestSpecBuilder();
		if (reqType.equals("GET")) {
			builder.setBaseUri("http://restapi.adequateshop.com/");
			builder.setBasePath("/api/Tourist");
			rspec = builder.build();
			res = RestAssured.given().spec(rspec).get();
		} else if (reqType.equals("POST")) {
			try {
				payload = new String(Files.readAllBytes(Paths
						.get(System.getProperty("user.dir") + "/src/main/resources/payload/" + payloadName + ".json")));
				jsonPayload = new JSONObject(payload);
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			updatedPayload = ApiUtility.setProperty(jsonPayload, key, value);
			builder.setBaseUri(baseUri);
			builder.setBasePath(basePath);
			builder.setBody(updatedPayload.toString());
			rspec = builder.build();
			res = RestAssured.given().spec(rspec).post();
		}
		return res;

	}

	public static JSONObject setProperty(JSONObject js1, String keys, String valueNew) throws JSONException {
		String[] keyMain = keys.split("\\.");
		for (String keym : keyMain) {
			Iterator iterator = js1.keys();
			String key = null;
			while (iterator.hasNext()) {
				key = (String) iterator.next();
				if ((js1.optJSONArray(key) == null) && (js1.optJSONObject(key) == null)) {
					if ((key.equals(keym))) {
						js1.put(key, valueNew);
						return js1;
					}
				}
				if (js1.optJSONObject(key) != null) {
					if ((key.equals(keym))) {
						js1 = js1.getJSONObject(key);
						break;
					}
				}
				if (js1.optJSONArray(key) != null) {
					JSONArray jArray = js1.getJSONArray(key);
					for (int i = 0; i < jArray.length(); i++) {
						js1 = jArray.getJSONObject(i);
					}
					break;
				}
			}
		}
		return js1;
	}

	{

	}

}
