import requests
import pytest
import allure
from urls import ORDERS



class TestCreateOrder:
    @allure.title("Создание заказа")
    @allure.description("Проверка создания заказа с разными цветами")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_with_color(self, color):

        with allure.step("Формирование payload"):
            payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "Saske, come back to Konoha",
                "color": color
            }

        with allure.step("Отправка запроса"):
            response = requests.post(
                ORDERS,
                json=payload
            )

        with allure.step("Проверка результата"):
            assert response.status_code == 201
            assert "track" in response.json()



    @allure.title("Создание заказа без цвета")
    @allure.description("Проверка создания заказа без поля color")
    def test_create_order_without_color(self):

        with allure.step("Формирование payload"):
            payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "Saske, come back to Konoha"
            }

        with allure.step("Отправка запроса"):
            response = requests.post(
                ORDERS,
                json=payload
            )

        with allure.step("Проверка результата"):
            assert response.status_code == 201
            assert "track" in response.json()    





