from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
import allure


@allure.suite("Тесты на проверку метода GET v1/account")
@allure.sub_suite("Получение текущего пользователя")
class TestGetV1Account:

    @allure.title("Проверка получения текущего неаутентифицированного пользователя")
    def test_get_v1_account_auth(self, auth_account_helper):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        GetV1Account.check_response_values(response)

    @allure.title("Проверка получения текущего неаутентифицированного пользователя")
    def test_get_v1_account_no_auth(self, account_helper):
        with check_status_code_http(401, "User must be authenticated"):
            account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)