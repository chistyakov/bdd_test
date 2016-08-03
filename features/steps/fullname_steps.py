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

@then('server returns JSON with full name of the user')
def step_impl(context):
    assert context.response.headers['Content-Type'] == 'application/json'
    assert context.response.json() == {
            'name': 'Alexander',
            'surname': 'Chistyakov',
            'patronymic': 'Olegovich'
        }

@given('the user does not exist on server')
def step_impl(context):
    context.server.drop_user_by_id(1)

@then('server returns 404')
def step_impl(context):
    assert context.response.status_code == 404

@when('we send request with malformed query')
def step_impl(context):
    context.response = requests.get('http://127.0.0.1:8080/?id==1')

@then('server returns 400')
def step_impl(context):
    assert context.response.status_code == 400

@when('we send request with not supported Content-Type')
def step_impl(context):
    context.response = requests.get('http://127.0.0.1:8080/?id=1', headers={'Content-Type': 'application/xml'})

@then('server returns 415')
def step_impl(context):
    assert context.response.status_code == 415

@given('there are users on server')
def step_impl(context):
    test_user_data1 = {
            'id': 1,
            'name': 'Alexander',
            'surname': 'Chistyakov',
            'patronymic': 'Olegovich'
        }
    test_user_data2 = {
            'id': 2,
            'name': 'Roman',
            'surname': 'Dmitrachenkov',
            'patronymic': 'Valerievich'
        }
    context.server.add_user(test_user_data1)
    context.server.add_user(test_user_data2)

@when('we send request with {id}')
def step_impl(context, id):
    context.response = requests.get('http://127.0.0.1:8080/?id={0}'.format(id))

@then('server returns {code}')
def step_impl(context, code):
    assert context.response.status_code == int(code)
