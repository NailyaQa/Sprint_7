import pytest
import requests

from urls import LOGIN_COURIER, CREATE_COURIER

@pytest.fixture
def delete_courier():
    courier_data = {}

    yield courier_data

    if courier_data:
        login_payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }

        login_response = requests.post(
            LOGIN_COURIER,
            data=login_payload
        )

        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]

            requests.delete(
                f"{CREATE_COURIER}/{courier_id}"
            )