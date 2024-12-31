import allure
from allure_commons.types import Severity

from data.models.request_models import ProjectRequest
from data.models.response_models import AllProjectsResponse, ProjectResponse
from data.project_constants import Color, ViewStyle
from utils import api


@allure.epic('Projects')
@allure.story('Get project')
@allure.title('[Project] Get. Existing project.')
@allure.description('Existing project should be accessible')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_get_project(session, create_new_project):
    new_project = create_new_project

    with allure.step(f'Get project with id: {new_project.id}'):
        resp = api.get_project(session, project_id=new_project.id)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Validate response json schema'):
        project_response = ProjectResponse.model_validate(resp.json())

    with allure.step('Validate field values'):
        assert project_response.name == new_project.name
        assert project_response.id == new_project.id
        assert project_response.parent_id is None
        assert project_response.order == 1
        assert project_response.color == Color.CHARCOAL
        assert project_response.comment_count == 0
        assert project_response.is_shared == False
        assert project_response.is_favorite == False
        assert project_response.is_inbox_project == False
        assert project_response.is_team_inbox == False
        assert project_response.view_style == ViewStyle.LIST


@allure.epic('Projects')
@allure.story('Get project')
@allure.title('[Project] Get. Full list of projects.')
@allure.description('List of all the projects should be accessible')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_get_all_projects(session, create_new_project):
    default_project_count = 1
    expected_projects = {'Inbox', create_new_project.name}

    with allure.step('Get all projects'):
        resp = api.get_all_projects(session)

    with allure.step('Assert response code is 200'):
        assert resp.status_code == 200

    with allure.step('Validate response json schema'):
        projects_response = AllProjectsResponse.model_validate(resp.json())

    with allure.step(f'Assert projects count is {default_project_count + 1}'):
        assert len(projects_response) == default_project_count + 1

    with allure.step(f'Assert projects\' names match expected values'):
        actual_projects = set([proj.name for proj in projects_response])
        assert actual_projects == expected_projects


@allure.epic('Authorization')
@allure.story('Get project')
@allure.title('[Project][Unauthorized] Get.')
@allure.description('Project can not be retrieved with unauthorized request.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_get_project__unauthorized(unauthorized_session, create_new_project):
    new_project = create_new_project
    with allure.step('Make an unauthorized request'):
        resp = api.get_project(unauthorized_session, project_id=new_project.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401


@allure.epic('Authorization')
@allure.story('Get project')
@allure.title('[Project][Invalid token] Get.')
@allure.description('Project can not be retrieved with invalid token used.')
@allure.tag('Regression', 'Security')
@allure.severity(Severity.BLOCKER)
def test_get_project__invalid_token(invalid_auth_session, create_new_project):
    new_project = create_new_project
    with allure.step('Make a request with invalid token'):
        resp = api.get_project(invalid_auth_session, project_id=new_project.id)
    with allure.step('Assert response code is 401'):
        assert resp.status_code == 401
