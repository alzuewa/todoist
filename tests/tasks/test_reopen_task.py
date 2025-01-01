import allure
from allure_commons.types import Severity

from data.models.request_models import TaskRequest
from utils import api


@allure.epic('Tasks')
@allure.story('Reopen task')
@allure.title('[Task] Reopen. Existing task.')
@allure.description('Existing closed task can be reopened')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
def test_reopen_existing_task(session, create_new_task):
    new_task = create_new_task
    with allure.step(f'Close task: id={new_task.id}, content={new_task.content}'):
        api.close_task(session, task_id=new_task.id)
    with allure.step('Reopen closed task'):
        resp = api.reopen_task(session, task_id=new_task.id)
    with allure.step('Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step('Assert reopened task is now in all active tasks list'):
        all_active_tasks = api.get_all_tasks(session).json()
        assert new_task.id in [task['id'] for task in all_active_tasks]


@allure.epic('Authorization')
@allure.story('Reopen task')
@allure.title('[Task][Unauthorized] Reopen.')
@allure.description('Task can not be reopened with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_reopen_task__unauthorized(session, unauthorized_session, create_new_task):
    new_task = create_new_task
    with allure.step('Close task with valid authorization'):
        api.close_task(session, task_id=new_task.id)
    with allure.step('Make an unauthorized request'):
        resp = api.reopen_task(unauthorized_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.story('Reopen task')
@allure.title('[Task][Invalid token] Reopen.')
@allure.description('Task can not be reopened with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_reopen_task__invalid_token(session, invalid_auth_session, create_new_task):
    new_task = create_new_task
    with allure.step('Close task with valid authorization'):
        api.close_task(session, task_id=new_task.id)
    with allure.step('Make a request with invalid token'):
        resp = api.reopen_task(invalid_auth_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
