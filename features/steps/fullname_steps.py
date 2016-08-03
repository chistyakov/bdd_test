from behave import given, when, then, step
import requests

@given('the user exists on server')
def step_impl(context):
    test_user_data = {
            'id': 1,
            'name': 'Alexander',
            'surname': 'Chistyakov',
            'patronymic': 'Olegovich'
        }
    context.server.add_user(test_user_data)

@when('we request the user by id')
def step_impl(context):
    context.response = requests.get('http://127.0.0.1:8080/?id=1')

@then('server returns 200')
def step_impl(context):
    assert context.response.status_code == 200
