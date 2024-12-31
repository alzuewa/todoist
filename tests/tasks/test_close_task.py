import allure
from allure_commons.types import Severity

from utils import api


@allure.epic('Tasks')
@allure.story('Close task')
@allure.title('[Task] Close. Existing task.')
@allure.description('Existing task can be deleted')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_close_existing_task(session, create_new_task):
    new_task = create_new_task
    with allure.step(f'Close task: {new_task.id=}, {new_task.content=}'):
        resp = api.close_task(session, task_id=new_task.id)
    with allure.step('Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step('Assert closed task is not in all active tasks list'):
        all_active_tasks = api.get_all_tasks(session).json()
        assert new_task.id not in [task['id'] for task in all_active_tasks]


@allure.epic('Tasks')
@allure.story('Close task')
@allure.title('[Task] Close. Not existing task.')
@allure.description('Not existing task can not be deleted')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
def test_close_not_existing_task(session):
    with allure.step(f'Close not existing task: id=987'):
        resp = api.close_task(session, task_id='987')
    with allure.step('Assert response code is 404 and error message'):
        assert resp.status_code == 404
        assert resp.text == 'Task not found'
