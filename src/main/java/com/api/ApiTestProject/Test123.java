package com.api.ApiTestProject;

import org.json.JSONObject;

import io.restassured.RestAssured;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.response.Response;
import io.restassured.specification.*;

public class Test123 {

	public static void main(String[] args) {
		RequestSpecBuilder builder = new RequestSpecBuilder();
//		builder.setBasePath("https://reqres.in/");
//		builder.addParam("/api/users");
		builder.setBaseUri("https://reqres.in/");
		builder.setBasePath("/api/users");
//		builder.addQueryParam("page", 2);
		builder.addQueryParam("page", 1);
	
		RequestSpecification spec = builder.build();
		Response res = RestAssured.given().spec(spec).when().get();
		System.out.println("---------------------"+ res.getStatusCode());
		System.out.println(res.getBody().toString());
		JSONObject json= new JSONObject(res.getBody().asString());
		System.out.println(json.get("total"));

//		JSONObject obj = new JSONObject(res.getBody());
//		for (int i = 0; i < obj.length(); i++) {
//			int expectedId = (Integer) obj.getJSONArray("data").getJSONObject(i).get("email");
//			if (expectedId == 3)
//				li.add((String) obj.getJSONArray("data").getJSONObject(i).get("email"));
//		}

	}

}
