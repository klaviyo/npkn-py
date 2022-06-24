import pytest
from npkn.api import APIClient


@pytest.fixture()
def client():
    user_id = "abcde12345"
    secret_key = "password"
    return APIClient(user_id, secret_key)

