import pytest
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account
import allure

@allure.suite("Тесты на проверку метода POST v1/account")
@allure.sub_suite("Регистрация нового пользователя")
class TestPostV1Account:

    @allure.title("Проверка регистрации пользователя с корректными данными")
    def test_post_v1_account(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        prefix_login = "joy_"
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response, prefix_login)

    @allure.title("Проверка регистрации пользователя с некорректными данными")
    @pytest.mark.parametrize('login, password, email', [
        ('X', '123445678', 'AnnaKurt@mail.ru'),
        ('AnnaKurt', '1', 'AnnaKurt@mail.ru'),
        ('AnnaK', '12345678', 'AnnaK2mail.ru'),
    ])
    def test_post_v1_account_negative(self, account_helper, login, password, email):
        with check_status_code_http(400, "Validation failed"):
            account_helper.register_new_user(login=login, password=password, email=email)