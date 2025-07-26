from selenium import webdriver
import pytest

driver = None
@pytest.fixture(scope="module")
def init_driver():
    global driver
    print("--------------------Set Up--------------------")
    driver= webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.delete_all_cookies()
    driver.maximize_window()
    driver.get("https://www.google.com/")
    yield
    print("--------------------Tear Down--------------------")
    driver.quit()

def test_webpage_login_gmail(init_driver):
    assert driver.title == "Google"

def test_webpage_login_gmail_url(init_driver):
    print(driver.current_url)
    assert driver.current_url == "https://www.google.com/"

# @pytest.userfixture(init_driver)
# def test_webpage_login_gmail_url():
#     print(driver.current_url)
#     assert driver.current_url == "https://www.google.com/"




