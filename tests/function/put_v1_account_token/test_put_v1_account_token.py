import allure

@allure.suite("Тесты на проверку метода POST v1/account/token")
@allure.sub_suite("Получение токена пользователя")
class TestPostV1AccountToken:

    @allure.title("Проверка получения токена нового пользователя с корректными данными")
    def test_post_v1_account_token(self, account_helper,prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
