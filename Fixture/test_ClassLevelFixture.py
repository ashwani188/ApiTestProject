import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def init_chrome_driver(request):
    driver_ch = webdriver.Chrome()
    request.cls.driver = driver_ch
    driver_ch.implicitly_wait(10)
    driver_ch.delete_all_cookies()
    driver_ch.maximize_window()
    driver_ch.get("https://www.google.com/")
    yield
    driver_ch.quit()


@pytest.fixture(scope="class")
def init_firefox_driver(request):
    driver_fx = webdriver.Firefox()
    # driver is passing to parent class through request.cls.driver
    request.cls.driver = driver_fx
    driver_fx.implicitly_wait(10)
    driver_fx.delete_all_cookies()
    driver_fx.maximize_window()
    driver_fx.get("https://www.Facebook.com/")
    yield
    driver_fx.close()


@pytest.mark.usefixtures("init_chrome_driver")
class TestBaseGoogleChrome:
    pass

class TestChildGoogleChrome(TestBaseGoogleChrome):
    def test_chrome_url(self):
        self.driver.get("https://www.google.com/")
        assert self.driver.title == "Google"
        assert self.driver.current_url == "https://www.google.com/"

@pytest.mark.usefixtures("init_firefox_driver")
class TestBaseGoogleFirefox:
    pass

class TestChildGoogleFirefox(TestBaseGoogleFirefox):
    def test_firefox_url(self):
        # driver is coming from parent class and parent class is using fixture to get driver
        self.driver.get("https://www.google.com/")
        assert self.driver.title == "Google"
        assert self.driver.current_url == "https://www.google.com/"