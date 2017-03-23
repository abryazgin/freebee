from behave import given, when, then, step
from models import user
from models import db_worker
import random


@given('user list')
def step_impl(contex):
    """ Сохраняет в contex.user_list всех пользователей из бд.
    """
    with db_worker.connection() as cursor:
        contex.user_list = user.User.get_all_users(conn=cursor)


@given('user with login "{login}"')
def step_impl(contex, login):
    """ Сохраняет в contex.db_user пользователя с заданным логином.
    """
    with db_worker.connection() as cursor:
        contex.db_user = user.User.get_user_by_login(conn=cursor,
                                                     log=login)


@given('user with id = {id:d}')
def step_impl(contex, id):
    """ Сохраняет в contex.db_user пользователя с заданным id.
    """
    with db_worker.connection() as cursor:
        contex.db_user = user.User.get_user_by_id(conn=cursor,
                                                  id=id)


@given('random user create')
def stem_impl(contex):
    """ Создаёт пользователя contex.new_user со случайными аттрибутами
    """
    rand_num = str(random.randint(a=100, b=1000000))
    contex.new_user = user.User(
        login=str(rand_num),
        email=str(rand_num) + '@smth.com',
        password=str(rand_num),
        role=random.choice([user.User.ADMIN,
                           user.User.CLIENT,
                           user.User.STAFFER])
    )
    contex.new_user_login = str(rand_num)
    with db_worker.connection() as cursor:
        contex.new_user.create(conn=cursor)


@given('new user')
def step_impl(contex):
    """ Читает из бд нового пользователя в contex.read_user
    """
    with db_worker.connection() as cursor:
        contex.read_user = user.User.get_user_by_login(
            conn=cursor,
            log=contex.new_user_login)
