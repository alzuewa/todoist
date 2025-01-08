import allure
from allure_commons.types import Severity

import api.tasks


@allure.epic('Tasks')
@allure.story('Close task')
@allure.title('[Task] Close. Existing task.')
@allure.description('Existing task can be deleted')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_close_existing_task(session, create_new_task):
    new_task = create_new_task
    with allure.step(f'Close task: id={new_task.id}, content={new_task.content}'):
        resp = api.tasks.close_task(session, task_id=new_task.id)
    with allure.step('Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step('Assert closed task is not in all active tasks list'):
        all_active_tasks = api.tasks.get_all_tasks(session).json()
        assert new_task.id not in [task['id'] for task in all_active_tasks]


@allure.epic('Tasks')
@allure.story('Close task')
@allure.title('[Task] Close. Not existing task.')
@allure.description('Not existing task can not be deleted')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
def test_close_not_existing_task(session):
    with allure.step(f'Close not existing task: id=987'):
        resp = api.tasks.close_task(session, task_id='987')
    with allure.step('Assert response code is 404 and error message'):
        assert resp.status_code == 404
        assert resp.text == 'Task not found'


@allure.epic('Authorization')
@allure.title('[Task][Unauthorized] Close.')
@allure.description('Task can not be closed with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_close_task__unauthorized(unauthorized_session, create_new_task):
    new_task = create_new_task
    with allure.step('Make an unauthorized request'):
        resp = api.tasks.close_task(unauthorized_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Task][Invalid token] Close.')
@allure.description('Task can not be closed with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_close_task__invalid_token(invalid_auth_session, create_new_task):
    new_task = create_new_task
    with allure.step('Make a request with invalid token'):
        resp = api.tasks.close_task(invalid_auth_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
