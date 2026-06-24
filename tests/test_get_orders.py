import requests
import allure
from urls import ORDERS

class TestGetOrders:

    @allure.title("Получение списка заказов")
    @allure.description("Проверка, что API возвращает список заказов")
    def test_get_orders_returns_list(self):
        with allure.step("Отправка GET запроса"):
            response = requests.get(
                ORDERS
            )

        with allure.step("Проверка статуса"):
            assert response.status_code == 200

        with allure.step("Проверка структуры ответа"):
            data = response.json()
            assert "orders" in data
            assert isinstance(data["orders"], list)