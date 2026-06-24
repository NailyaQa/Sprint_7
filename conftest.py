import pytest
import requests

from urls import CREATE_COURIER

@pytest.fixture
def delete_courier():
    # фикстура возвращает функцию удаления
    def _delete_courier(courier_id):
        response = requests.delete(
            f"{CREATE_COURIER}/{courier_id}"
        )
        return response

    return _delete_courier