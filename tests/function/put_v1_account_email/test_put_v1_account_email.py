def test_post_v1_account_email(account_helper,prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.rename_email(login=login, password=password)
    account_helper.user_login_after_rename_email(login=login, password=password)
    account_helper.user_login(login=login, password=password)
