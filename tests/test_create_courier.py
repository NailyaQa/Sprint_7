import requests
import random
import string
import allure
from helpers.generator import generate_courier_data

from urls import CREATE_COURIER
from urls import LOGIN_COURIER



class TestCreateCourier:

    @allure.title("Создание курьера")
    @allure.description("Проверка успешного создания курьера ")
    def test_create_courier_success(self, delete_courier):

        with allure.step("Генерация данных курьера"):
            payload = generate_courier_data()

            
        with allure.step("Создание курьера"):
            create_response = requests.post(
                CREATE_COURIER,
                data=payload
            )

            delete_courier["login"] = payload["login"]
            delete_courier["password"] = payload["password"]

        with allure.step("Проверка успешного создания"):
            assert create_response.status_code == 201
            assert create_response.json()["ok"] is True

        

    @allure.title("Нельзя создать дубликат курьера")
    @allure.description("Проверка ошибки при повторном создании курьера с теми же данными")
    def test_create_duplicate_courier(self, delete_courier):

        with allure.step("Генерация данных курьера"):
            payload = generate_courier_data()

        with allure.step("Первое создание курьера"):
            first_response = requests.post(
                CREATE_COURIER,
                data=payload
            )
            assert first_response.status_code == 201

        # Сообщаем фикстуре, какого курьера удалить после завершения теста
        delete_courier["login"] = payload["login"]
        delete_courier["password"] = payload["password"]

        with allure.step("Попытка создать дубликат"):
            second_response = requests.post(
            CREATE_COURIER,
            data=payload
        )

            assert second_response.status_code == 409
            assert second_response.json()["message"] == "Этот логин уже используется. Попробуйте другой."


    @allure.title("Создание курьера без логина")
    @allure.description("Проверка ошибки при отсутствии обязательного поля login")
    def test_create_courier_without_login(self):

        with allure.step("Генерация данных без login"):
            letters = string.ascii_lowercase

            password = ''.join(random.choice(letters) for _ in range(10))
            first_name = ''.join(random.choice(letters) for _ in range(10))

            payload = {
                "password": password,
                "firstName": first_name
            }

        with allure.step("Отправка запроса"):
            response = requests.post(
                CREATE_COURIER,
                data=payload
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"


    @allure.title("Создание курьера без пароля")
    @allure.description("Проверка ошибки при отсутствии обязательного поля password")
    def test_create_courier_without_password(self):

        with allure.step("Генерация данных без password"):
            letters = string.ascii_lowercase

            login = ''.join(random.choice(letters) for _ in range(10))
            first_name = ''.join(random.choice(letters) for _ in range(10))

            payload = {
                "login": login,
                "firstName": first_name
            }

        with allure.step("Отправка запроса"):
            response = requests.post(
                CREATE_COURIER,
                data=payload
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
