import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def intializeBrowser(request):
    driver = webdriver.Chrome()
    request.cls.driver = driver

    yield
    request.cls.driver.quit()