from behave import given, when, then, step
from models import user
from models import db_worker


@then('user role is "{role}"')
def step_imp(context, role):
    """ Проверяет соответствие роли у context.db_user заданной.
    """
    assert context.db_user.role == role


@then('user enable changed')
def step_impl(contex):
    """ Проверяет, изменено ли в бд свойство enable contex.db_user
    """
    with db_worker.connection() as cursor:
        contex.changed_user = user.User.get_user_by_login(
            conn=cursor,
            log=contex.db_user.login)
        assert contex.changed_user.enable != contex.enable_before


@then('user must be the same')
def step_impl(contex):
    """ Проверяет соответствие contex.new_user и contex.read_user
    """
    assert contex.new_user.equal(contex.read_user)
