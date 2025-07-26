from selenium import webdriver
import pytest


@pytest.fixture(scope="class" ,params=["chrome", "firefox"])
def init_browser(request):
    if request.param== "chrome":
      driver = webdriver.Chrome()
    elif request.param== "firefox":
       driver = webdriver.Firefox()
    request.cls.driver = driver

    yield
    request.cls.driver.quit()










