import pytest
from pytest import MonkeyPatch
import requests_mock

with MonkeyPatch.context() as mp:
    mp.delenv("NPKN_API_HOST", raising=False)
    from npkn.api import APIClient


MOCK_USER_UID = "abcde12345"
MOCK_SECRET_KEY = "password"


@pytest.fixture()
def client():
    return APIClient(MOCK_USER_UID, MOCK_SECRET_KEY)


def test_get_success(client):
    expected_res = {"data": "success"}

    with requests_mock.Mocker() as mock:
        request_headers = {
            "napkin-user-uid": MOCK_USER_UID,
            "napkin-api-key": MOCK_SECRET_KEY
        }
        mock.get("https://api.napkin.io/api/1/account", request_headers=request_headers, json=expected_res)

        res, err = client.get("account")

        assert not err
        assert res == expected_res


def test_get_error(client):
    expected_res = {"error": "Something went wrong."}

    with requests_mock.Mocker() as mock:
        request_headers = {
            "napkin-user-uid": MOCK_USER_UID,
            "napkin-api-key": MOCK_SECRET_KEY
        }
        mock.get("https://api.napkin.io/api/1/account", status_code=400, request_headers=request_headers, json=expected_res)

        res, err = client.get("account")

        assert not res
        assert err == expected_res


def test_post_success(client):
    expected_res = {"data": "success"}

    with requests_mock.Mocker() as mock:
        request_headers = {
            "napkin-user-uid": MOCK_USER_UID,
            "napkin-api-key": MOCK_SECRET_KEY
        }
        mock.post("https://api.napkin.io/api/1/run", request_headers=request_headers, json=expected_res)

        res, err = client.post("run")

        assert not err
        assert res == expected_res


def test_post_error(client):
    expected_res = {"error": "Something went wrong."}

    with requests_mock.Mocker() as mock:
        request_headers = {
            "napkin-user-uid": MOCK_USER_UID,
            "napkin-api-key": MOCK_SECRET_KEY
        }
        mock.post("https://api.napkin.io/api/1/run", status_code=400, request_headers=request_headers, json=expected_res)

        res, err = client.post("run")

        assert not res
        assert err == expected_res



