from selenium import webdriver

driver =None
def setup_module(module):
    global driver
    driver= webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.delete_all_cookies()
    driver.maximize_window()
    driver.get("https://www.google.com/")

def teardown_module(module):
    driver.quit()

def test_webpage_login_gmail():
    assert driver.title == "Google"

def test_webpage_login_gmail_url():
    print(driver.current_url)
    assert driver.current_url == "https://www.google.com/"



