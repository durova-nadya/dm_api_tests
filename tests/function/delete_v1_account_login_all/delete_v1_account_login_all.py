import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login/all")
@allure.sub_suite("Завершение сессии пользователя на всех устройствах")
class TestDeleteV1AccountLoginAll:

    @allure.title("Проверка завершения сессий аутентифицированного пользователя")
    def test_delete_v1_account_login_all_auth(self, auth_account_helper):
        response = auth_account_helper.dm_account_api.login_api.delete_v1_account_login_all()
        assert response.status_code == 204, "Сессии пользователя не завершены!"

    @allure.title("Проверка завершения сессий неаутентифицированного пользователя")
    def test_delete_v1_account_login_all(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)

        response = account_helper.user_login(login=login, password=password)
        token_1 = response.headers["x-dm-auth-token"]
        response = account_helper.user_login(login=login, password=password)
        token_2 = response.headers["x-dm-auth-token"]

        account_helper.user_logout_all(token_1)









