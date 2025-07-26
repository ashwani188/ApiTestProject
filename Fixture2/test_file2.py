import pytest

def test_divisible_by_5(test_cofiguration):
    assert test_cofiguration%5==0

def test_divisible_by_10(test_cofiguration):
    assert test_cofiguration%10==0

def test_divisible_by_7(test_cofiguration):
    assert test_cofiguration%7==0