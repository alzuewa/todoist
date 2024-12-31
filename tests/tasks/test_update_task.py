import allure
import pytest
from allure_commons.types import Severity

from data.models.request_models import TaskRequest
from data.models.response_models import TaskResponse
from utils import api


@allure.epic('Tasks')
@allure.story('Update task')
@allure.title('[Task] Update. Description.')
@allure.description('Task description can be updated')
@allure.tag('Edit', 'New feature')
@allure.severity(Severity.NORMAL)
def test_update_task_description(session, create_new_task):
    new_task = create_new_task
    with allure.step('Update task description'):
        updated_fields = TaskRequest(description='1 loaf')
        resp = api.update_task(session, task_id=new_task.id, json=updated_fields)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Validate response json schema'):
        task_response = TaskResponse.model_validate(resp.json())

    with allure.step('Validate the task description has been updated'):
        assert task_response.id == new_task.id
        assert task_response.description == updated_fields.description


@allure.epic('Tasks')
@allure.story('Update task')
@allure.title('[Task] Update. Priority. Invalid values.')
@allure.description('Task priority can be updated within a specific range of numbers')
@allure.tag('Edit', 'New feature')
@allure.severity(Severity.NORMAL)
@pytest.mark.parametrize('priority', [-1, 0, 5])
def test_task_update__invalid_priority(session, create_new_task, priority):
    new_task = create_new_task

    with allure.step(f'Update task priority with invalid value: {priority=}'):
        updated_fields = TaskRequest(priority=priority)
        resp = api.update_task(session, task_id=new_task.id, json=updated_fields)

    with allure.step('Validate response json schema'):
        task_response = TaskResponse.model_validate(resp.json())

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Assert task priority value has not changed'):
        assert task_response.priority == new_task.priority
