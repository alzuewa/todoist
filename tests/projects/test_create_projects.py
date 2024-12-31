import allure
import pytest
from allure_commons.types import Severity

from data.models.request_models import ProjectRequest
from data.models.response_models import ProjectResponse
from data.project_constants import Color, ViewStyle
from utils import api


@allure.epic('Projects')
@allure.story('Create project')
@allure.title('[Project] Create. Required field only.')
@allure.description('Project can be created with 1 required field: project name')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_create_project__only_required_param(session):
    with allure.step(f'Create the project with name: Shopping list'):
        new_project = ProjectRequest(name='Shopping list')
        resp = api.create_project(session, json=new_project)

    with allure.step(f'Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step(f'Validate json response schema'):
        project_response = ProjectResponse.model_validate(resp.json())

    with allure.step(f'Validate fields\' values'):
        assert project_response.name == new_project.name
        assert project_response.comment_count == 0
        assert project_response.color == Color.CHARCOAL
        assert project_response.is_shared == False
        assert project_response.order == 1
        assert project_response.is_favorite == False
        assert project_response.is_inbox_project == False
        assert project_response.is_team_inbox == False
        assert project_response.view_style == ViewStyle.LIST
        assert project_response.parent_id is None


@allure.epic('Projects')
@allure.story('Create project')
@allure.title('[Project] Create. All the fields.')
@allure.description('Project can be created with several fields at once')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_create_project__all_params(session, create_new_project):
    parent_project = create_new_project

    with allure.step(f'Create the project with all the params filled'):
        child_project = ProjectRequest(
            name='Shopping list inner',
            parent_id=parent_project.id,
            color=Color.YELLOW,
            is_favorite=True,
            view_style=ViewStyle.LIST
        )
        resp = api.create_project(session, json=child_project)

    with allure.step(f'Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step(f'Validate json response schema'):
        project_response = ProjectResponse.model_validate(resp.json())

    with allure.step(f'Validate fields\' values'):
        assert project_response.name == child_project.name
        assert project_response.comment_count == 0
        assert project_response.color == Color.YELLOW
        assert project_response.is_shared == False
        assert project_response.order == 1
        assert project_response.is_favorite == True
        assert project_response.is_inbox_project == False
        assert project_response.is_team_inbox == False
        assert project_response.view_style == ViewStyle.LIST
        assert project_response.parent_id == parent_project.id


@allure.epic('Projects')
@allure.story('Create project')
@allure.title('[Project] Create. Required field missed.')
@allure.description('Project can not be created without required field')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_create_project__required_param_missed(session):
    with allure.step(f'Create project without body in request'):
        resp = api.create_project(session)
    with allure.step(f'Assert response code is 400 and error message'):
        assert resp.status_code == 400
        assert resp.text == 'Name must be provided for the project creation'


@allure.epic('Projects')
@allure.story('Create project')
@allure.title('[Project] Create. Required field invalid value.')
@allure.description('Project can not be created with invalid required field values: "", " "')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
@pytest.mark.parametrize('name', ['', ' '])
def test_create_project__required_param_invalid_value(session, name):
    with allure.step(f'Create project with invalid name: "{name}"'):
        new_project = ProjectRequest(name=name)
        resp = api.create_project(session, json=new_project)
    with allure.step(f'Assert response code is 400 and error message'):
        assert resp.status_code == 400
        assert resp.text == 'Name must be provided for the project creation'
