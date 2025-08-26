import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login")
@allure.sub_suite("Завершение сессии пользователя")
class TestDeleteV1AccountLogin:

    @allure.title("Проверка завершения сессии аутентифицированного пользователя")
    def test_delete_v1_account_login_auth(self, auth_account_helper):
        auth_account_helper.dm_account_api.login_api.delete_v1_account_login()

    @allure.title("Проверка завершения сессии неаутентифицированного пользователя")
    def test_delete_v1_account_login_no_auth(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password)
        token = response.headers["x-dm-auth-token"]
        account_helper.user_logout(token=token)