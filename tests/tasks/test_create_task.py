import allure
from allure_commons.types import Severity

from config import config
from data.models.request_models import TaskRequest
from data.models.response_models import TaskResponse
from utils import api


@allure.epic('Tasks')
@allure.story('Create task')
@allure.title('[Task] Create. Required field only.')
@allure.description('Task can be created with 1 required field: task content')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_create_task__only_required_param(session):
    with allure.step(f'Create task with name: Buy bread'):
        new_task = TaskRequest(content='Buy bread')
        resp = api.create_task(session, json=new_task)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step(f'Validate json response schema'):
        task_response = TaskResponse.model_validate(resp.json())

    with allure.step(f'Validate fields\' values'):
        assert task_response.content == new_task.content
        assert task_response.labels == []
        assert task_response.is_completed == False
        assert task_response.due is None
        assert task_response.duration is None
        assert task_response.priority == 1
        assert task_response.order == 1
        assert task_response.project_id == config.inbox_id
        assert task_response.section_id is None
        assert task_response.parent_id is None


@allure.epic('Tasks')
@allure.story('Create task')
@allure.title('[Task] Create. Several fields.')
@allure.description('Task can be created with several fields at once')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_create_task_many_params(session, create_new_project):
    project = create_new_project
    with allure.step(f'Create task with several params'):
        new_task = TaskRequest(
            content='Buy bread',
            project_id=project.id,
            priority=3,
            labels=['groceries', 'home']
        )
        resp = api.create_task(session, json=new_task)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step(f'Validate json response schema'):
        task_response = TaskResponse.model_validate(resp.json())

    with allure.step(f'Validate fields\' values'):
        assert task_response.content == new_task.content
        assert task_response.labels == new_task.labels
        assert task_response.is_completed == False
        assert task_response.due is None
        assert task_response.duration is None
        assert task_response.priority == 3
        assert task_response.order == 1
        assert task_response.project_id == project.id
        assert task_response.section_id is None
        assert task_response.parent_id is None


@allure.epic('Tasks')
@allure.story('Create task')
@allure.title('[Task] Create. Required field missed.')
@allure.description('Task can not be created without required field')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_create_task__required_param_missed(session):
    with allure.step(f'Create task without body in request'):
        resp = api.create_task(session)
    with allure.step(f'Assert response code is 400 and error message'):
        assert resp.status_code == 400
        assert resp.json()['error'] == 'Required argument is missing'