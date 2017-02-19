from behave import given, when, then, step
from models import user
from models import db_worker


@then('user role is "{role}"')
def step_imp(context, role):
    """
    Проверяет соответствие роли у context.user_by_login заданной.
    """
    assert context.user_by_login.role == role


@then('user enable changed')
def step_impl(contex):
    """
    Проверяет, изменено ли в бд свойство enable contex.user_by_login
    """
    with db_worker.connection() as cursor:
        contex.changed_user = user.User.get_user_by_login(
            cursor, contex.user_by_login.login)
        assert contex.changed_user.enable != contex.enable_before
