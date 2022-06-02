package com.api.ApiTestProject;

import java.io.FileInputStream;
import java.io.IOException;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class ExcelReader {
	Workbook wb = null;
	Sheet sheet = null;
	Row rwForSize = null;
	Row rw = null;
	int rowsCount;
	int cellCount;

	@SuppressWarnings({ "deprecation" })
	public Object[][] readExcel(String filePath, String sheetName) {
		Object[][] testDataApi = null;
		try {
			FileInputStream fis = new FileInputStream(System.getProperty("user.dir") + filePath);
			wb = new XSSFWorkbook(fis);
			sheet = wb.getSheet(sheetName);
			rwForSize = sheet.getRow(0);
			cellCount = rwForSize.getLastCellNum();
			rowsCount = sheet.getPhysicalNumberOfRows();
			testDataApi = new Object[rowsCount][cellCount];
			for (int i = 0; i < rowsCount; i++) {
				rw = sheet.getRow(i);
				for (int j = 0; j < cellCount; j++) {
					switch (rw.getCell(i).getCellType()) {
					case Cell.CELL_TYPE_STRING:
						testDataApi[i][j] = rw.getCell(j).getStringCellValue();
						break;

					case Cell.CELL_TYPE_NUMERIC:
						testDataApi[i][j] = rw.getCell(i).getNumericCellValue();
						break;
					}

				}
			}

		} catch (IOException e) {
			e.printStackTrace();
		}
		return testDataApi;

	}

}
