import allure

@allure.suite("Тесты на проверку метода POST v1/account/email")
@allure.sub_suite("Смена email нового пользователя")
class TestPostV1AccountEmail:

    @allure.title("Проверка смены email нового пользователя с корректными данными")
    def test_post_v1_account_email(self, account_helper,prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_email = 'new_' + email

        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
        account_helper.change_email(login=login, password=password, new_email=new_email)
        account_helper.user_login(login=login, password=password)
