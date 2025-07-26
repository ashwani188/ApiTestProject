import pytest

def test_method4():
    num1=8
    num2=8
    assert num1 == num2, "num1 should be equal to num2"

def test_method5():
    name="John"
    assert name.upper() == "JOHN"

def test_login_google():
    name="google"
    assert name=="google"
