from behave import given, when, then, step
from models import user
from models import db_worker


@given('user list')
def step_impl(context):
    """
    Сохраняет в context.usr_list список всех пользователей из бд.
    """
    with db_worker.connection() as cursor:
        context.usr_list = user.User.get_all_users(cursor)


@given('user with login "{login}"')
def step_impl(contex, login):
    """
    Сохраняет в contex.user_by_login пользователя с заданным логином.
    """
    with db_worker.connection() as cursor:
        contex.user_by_login = user.User.get_user_by_login(cursor, login)
