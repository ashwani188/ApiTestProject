import pytest

def test_divisible_by_5(test_cofiguration):
    assert test_cofiguration%5==0

def test_divisible_by_10(test_cofiguration):
    assert test_cofiguration%10==0

@pytest.mark.usefixtures("init_intialize")
class Base_Test:
    pass

class Test_Class_Leavel_Pearametrize(Base_Test):
    def test_webpage_login_google(self):
        self.driver.get("https://www.google.com/")
        assert self.driver.title == "Google"