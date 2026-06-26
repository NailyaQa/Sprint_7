from helpers.generator import register_new_courier_and_return_login_password
import requests
import random
import string
import allure
from urls import LOGIN_COURIER

class TestLoginCourier:
    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверка, что курьер может войти в систему с корректным логином и паролем")
    def test_login_courier_success(self):
        with allure.step("Создать нового курьера"):
            courier_data = register_new_courier_and_return_login_password()
            

            login = courier_data[0]
            password = courier_data[1]

        with allure.step("Отправить запрос на авторизацию"):
            payload = {
                "login": login,
                "password": password
            }

            response = requests.post(
                LOGIN_COURIER,
                data=payload
            )

        with allure.step("Проверить код ответа и наличие id"):   
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Авторизация с неверным логином")
    @allure.description("Проверка ошибки при вводе неверного логина")
    def test_login_without_login(self):
        
        with allure.step("Создать нового курьера"):    
            courier_data = register_new_courier_and_return_login_password()

            password = courier_data[1] 

            #  искажаем логин
            wrong_login = courier_data[0] + "123"

        with allure.step("Отправить запрос с неверным логином"):
            payload = {
                "login": wrong_login,
                "password": password
            }

            response = requests.post(
                LOGIN_COURIER,
                data=payload
            )
        with allure.step("Проверить сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена" 

    @allure.title("Авторизация с неверным паролем")
    @allure.description("Проверка ошибки при вводе неверного пароля")
    def test_login_without_password(self):
        

        with allure.step("Создать нового курьера"):
            courier_data = register_new_courier_and_return_login_password()

            wrong_password = courier_data[1]  + "123"

            login = courier_data[0] 

        with allure.step("Отправить запрос с неверным паролем"):
            payload = {
                "login": login,
                "password": wrong_password
            }

            response = requests.post(
                LOGIN_COURIER,
                data=payload
            )
        with allure.step("Проверить сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена" 

    @allure.title("Авторизация без логина")
    @allure.description("Проверка ошибки при отсутствии логина")
    def test_login_with_wrong_login(self):
            
        with allure.step("Создать нового курьера"):
            courier_data = register_new_courier_and_return_login_password()

            password = courier_data[1]

        with allure.step("Отправить запрос без логина"):
            payload = {
                "password": password
            }

            response = requests.post(
                LOGIN_COURIER,
                data=payload
            )
        with allure.step("Проверить сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Авторизация без пароля")
    @allure.description("Проверка ошибки при отсутствии пароля")
    def test_login_with_wrong_password(self):

        with allure.step("Создать нового курьера"):
            courier_data = register_new_courier_and_return_login_password()

            login = courier_data[0]
        with allure.step("Отправить запрос без пароля"):
            payload = {
            "login": login
            }   

            response = requests.post(
                LOGIN_COURIER,
            data=payload
            )
            #Тест реализован согласно документации. 
            #На момент проверки сервис возвращает 504 вместо ожидаемого 400,
            #что выглядит как проблема тестового стенда.
        with allure.step("Проверить сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Авторизация несуществующего курьера")
    @allure.description("Проверка ошибки при попытке входа под несуществующим пользователем")
    def test_login_nonexistent_courier(self):

        with allure.step("Сгенерировать данные несуществующего курьера"):
            letters = string.ascii_lowercase

            login = ''.join(random.choice(letters) for _ in range(10))
            password = ''.join(random.choice(letters) for _ in range(10))

    
            payload = {
                "login": login,
                "password": password
                }
        with allure.step("Отправить запрос на авторизацию"):
            response = requests.post(
                    LOGIN_COURIER,
                    data=payload
                )
        with allure.step("Проверить сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена" 