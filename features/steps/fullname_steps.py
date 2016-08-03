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

@then('server returns HTTP status code {code}')
def step_impl(context, code):
    assert context.response.status_code == int(code)


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


@when('we send request with malformed query')
def step_impl(context):
    context.response = requests.get('http://127.0.0.1:8080/?id==1')

@when('we send request with not supported Content-Type')
def step_impl(context):
    context.response = requests.get('http://127.0.0.1:8080/?id=1', headers={'Content-Type': 'application/xml'})


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

@when('we send request with {identificator}')
def step_impl(context, identificator):
    context.response = requests.get('http://127.0.0.1:8080/?id={0}'.format(identificator))

@when('we use not suppported HTTP method')
def step_impl(context):
    context.response = requests.post('http://127.0.0.1:8080/', data={'key':'value'})

@given('the user does not have surname')
def step_impl(context):
    test_user_no_surname = {
            'id': 1,
            'name': 'Aron',
            'patronymic': 'Gunnarsson'
        }
    context.server.add_user(test_user_no_surname)

@then('server returns JSON with empty surname of the user')
def step_impl(context):
    assert context.response.headers['Content-Type'] == 'application/json'
    print(context.response.json())
    assert context.response.json() == {'name': 'Aron', 'surname': '', 'patronymic': 'Gunnarsson'}
