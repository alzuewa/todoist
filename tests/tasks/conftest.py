import allure
import pytest

from data.models.request_models import TaskRequest
from data.models.response_models import TaskResponse
from utils import api


@pytest.fixture(scope='function')
def create_new_task(session):
    with allure.step(f'Create fixture task with name: Buy bread'):
        task = TaskRequest(content='Buy bread')
        resp = api.create_task(session, task)
        task_resp = TaskResponse.model_validate(resp.json())
        return task_resp


@pytest.fixture(scope='function', autouse=True)
def delete_all_tasks(session):
    yield

    with allure.step(f'Delete all tasks'):
        response = api.get_all_tasks(session).json()
        task_ids = [task['id'] for task in response]
        for task_id in task_ids:
            api.delete_task(session, task_id=task_id)
