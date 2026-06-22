import requests
import allure

class TestGetOrders:

    @allure.title("Получение списка заказов")
    @allure.description("Проверка, что API возвращает список заказов")
    def test_get_orders_returns_list(self):
        with allure.step("Отправка GET запроса"):
            response = requests.get(
                "https://qa-scooter.praktikum-services.ru/api/v1/orders"
            )

        with allure.step("Проверка статуса"):
            assert response.status_code == 200

        with allure.step("Проверка структуры ответа"):
            data = response.json()
            assert "orders" in data
            assert isinstance(data["orders"], list)