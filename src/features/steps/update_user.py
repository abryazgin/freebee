from behave import given, when, then, step
from models import user
from models import db_worker


@when('user enable changing')
def step_impl(contex):
    """ Сохраняет в contex.enable_before свойство enable пользователя
    contex.db_user и после изменяет его
    """
    contex.enable_before = contex.db_user.enable
    contex.db_user.enable = not contex.db_user.enable
    with db_worker.connection() as cursor:
        contex.db_user.update(conn=cursor)
