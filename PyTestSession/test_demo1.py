import pytest

def test_method1():
    assert True


def test_method2():
    assert False

def test_method3():
    num=3
    assert num == 4, "num should be equal to 3"

@pytest.mark.home
def test_method4():
    num1=8
    num2=8
    assert num1 == num2, "num1 should be equal to num2"

@pytest.mark.home
def test_method5():
    name="John"
    assert name.upper() == "JOHN"

def test_login_wahtsapp():
    name="wahtsapp"
    assert name=="wahtsapp"
