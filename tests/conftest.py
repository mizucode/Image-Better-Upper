import pytest


def sisi():
    return "cute"


@pytest.fixture()
def get_sisi():
    value = sisi()
    return value
