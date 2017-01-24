# -- FILE: features/steps/example_steps.py
from behave import given, when, then, step
from models import user
from models import db_worker


@given('we have behave installed')
def step_impl(context):
    pass


@when('we implement {number:d} tests')
def step_impl(context, number):  # -- NOTE: number is converted into integer
    assert number > 1 or number == 0
    context.tests_count = number


@then('behave will test them for us!')
def step_impl(context):
    assert context.failed is False
    assert context.tests_count >= 0


@given('connect to db')
def step_impl(context):
    context.db = db_worker.get_db()
    context.cursor = context.db.cursor(dictionary=True)


@when('get user with id = {num:d}')
def step_imp(context, num):
    context.us = user.User.get_user_by_id(
        context.cursor, num)
    assert context.us is not None


@then('user role should be "{role}"')
def step_imp(context, role):
    assert context.us.role == role
    context.cursor.close()
    context.db.close()
