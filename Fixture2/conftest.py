import pytest
from selenium import webdriver

@pytest.fixture
def test_cofiguration():
    total=10
    return total

@pytest.fixture(scope="class", params=["chrome", "firefox"])
def init_intialize(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    request.cls.driver= driver
    yield
    driver.close()
