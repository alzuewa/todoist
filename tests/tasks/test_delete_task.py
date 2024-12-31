import allure
from allure_commons.types import Severity

from utils import api


@allure.epic('Tasks')
@allure.story('Delete task')
@allure.title('[Task] Delete. Existing task.')
@allure.description('Existing task can be deleted')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_delete_task(session, create_new_task):
    new_task = create_new_task

    with allure.step(f'Delete task: {new_task.id=}, {new_task.content=}'):
        resp = api.delete_task(session, task_id=new_task.id)
    with allure.step('Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step('Assert deleted task can not be retrieved and 404 response code'):
        assert api.get_task(session, task_id=new_task.id).status_code == 404
