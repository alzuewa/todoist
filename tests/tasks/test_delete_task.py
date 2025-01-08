import allure
from allure_commons.types import Severity

import api.tasks


@allure.epic('Tasks')
@allure.story('Delete task')
@allure.title('[Task] Delete. Existing task.')
@allure.description('Existing task can be deleted')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_delete_task(session, create_new_task):
    new_task = create_new_task

    with allure.step(f'Delete task: id={new_task.id}, content={new_task.content}'):
        resp = api.tasks.delete_task(session, task_id=new_task.id)
    with allure.step('Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step('Assert deleted task can not be retrieved and 404 response code is returned'):
        assert api.tasks.get_task(session, task_id=new_task.id).status_code == 404


@allure.epic('Authorization')
@allure.title('[Task][Unauthorized] Delete.')
@allure.description('Task can not be deleted with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_delete_task__unauthorized(unauthorized_session, create_new_task):
    new_task = create_new_task
    with allure.step('Make an unauthorized request'):
        resp = api.tasks.delete_task(unauthorized_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.title('[Task][Invalid token] Delete.')
@allure.description('Task can not be deleted with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_delete_task__invalid_token(invalid_auth_session, create_new_task):
    new_task = create_new_task
    with allure.step('Make a request with invalid token'):
        resp = api.tasks.delete_task(invalid_auth_session, task_id=new_task.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
