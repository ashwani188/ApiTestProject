from selenium import webdriver



def test_webpage_login_facebook():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.facebook.com")
    assert driver.title == "Facebook"
    driver.quit()

def test_webpage_login_google():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.google.com")
    assert driver.title == "Google"
    driver.quit()

def test_webpage_login_youtube():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.youtube.com/")
    assert driver.title == "YouTube"
    driver.quit()

def test_webpage_login_gmail():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.gmail.com/")
    print(driver.title)
    assert driver.title == "Gmail"
    driver.quit()

