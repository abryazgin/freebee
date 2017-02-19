from behave import given, when, then, step
from models import user
from models import db_worker


@when('user enable changing')
def step_impl(contex):
    """
    Сохраняет в contex.enable_before свойство enable пользователя
    contex.user_by_login и после изменяет его
    """
    contex.enable_before = contex.user_by_login.enable
    contex.user_by_login.enable = not contex.user_by_login.enable
    with db_worker.connection() as cursor:
        contex.user_by_login.update(cursor)
