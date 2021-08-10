import pytest

from app import app

def sisi():
    return "cute"


@pytest.fixture()
def get_sisi():
    value = sisi()
    return value
