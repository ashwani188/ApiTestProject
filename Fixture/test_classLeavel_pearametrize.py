from selenium import webdriver
import pytest

@pytest.fixture(scope="class", params=["chrome", "firefox"])
def init_intialize(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    request.cls.driver= driver
    yield
    driver.close()

@pytest.mark.usefixtures("init_intialize")
class Base_Test:
    pass

class Test_Class_Leavel_Pearametrize(Base_Test):
    def test_webpage_login_google(self):
        self.driver.get("https://www.google.com/")
        assert self.driver.title == "Google"

    # def test_webpage_login_gmail_url(self, chrome_intialize):
    #     print(chrome_intialize.current_url)
    #     assert chrome_intialize.current_url == "https://www.google.com/"


