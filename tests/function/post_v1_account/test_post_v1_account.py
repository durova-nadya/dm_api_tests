import pytest
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response)


@pytest.mark.parametrize('login, password, email', [
    ('X', '123445678', 'AnnaKurt@mail.ru'),
    ('AnnaKurt', '1', 'AnnaKurt@mail.ru'),
    ('AnnaK', '12345678', 'AnnaK2mail.ru'),
])
def test_post_v1_account_negative(account_helper, login, password, email):
    with check_status_code_http(400, "Validation failed"):
        account_helper.register_new_user(login=login, password=password, email=email)





