import allure
import pytest

from config import config
from data.models.request_models import ProjectRequest
from data.models.response_models import ProjectResponse
from utils import api
from utils.session import ApiSession, BearerAuth


@pytest.fixture(scope='package', name='session')
def authorized_session():
    session = ApiSession(base_url=config.base_url, auth=BearerAuth(config.token))

    yield session


@pytest.fixture(scope='function')
def unauthorized_session():
    session = ApiSession(base_url=config.base_url)

    yield session


@pytest.fixture(scope='function', autouse=True)
def delete_all_projects(session):
    yield

    with allure.step(f'Delete all projects'):
        response = api.get_all_projects(session).json()
        project_ids = [project['id'] for project in response if project['name'] != 'Inbox']
        for project_id in project_ids:
            api.delete_project(session, project_id=project_id)


@pytest.fixture(scope='function')
def create_new_project(session):
    with allure.step(f'Create fixture project with name: Shopping list'):
        project = ProjectRequest(name='Shopping list')
        resp = api.create_project(session, project)
        project_resp = ProjectResponse.model_validate(resp.json())
        return project_resp
