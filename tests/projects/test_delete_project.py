import allure
from allure_commons.types import Severity

from utils import api


@allure.epic('Projects')
@allure.story('Delete project')
@allure.title('[Project] Delete. Existing project.')
@allure.description('After deletion project can not be accessed')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_delete_existing_project(session, create_new_project):
    new_project = create_new_project

    with allure.step(f'Delete project: {new_project.name}'):
        resp = api.delete_project(session, project_id=new_project.id)
    with allure.step(f'Assert response code is 204'):
        assert resp.status_code == 204
    with allure.step(f'Assert deleted project can not be retrieved and 404 response code'):
        assert api.get_project(session, project_id=new_project.id).status_code == 404


@allure.epic('Projects')
@allure.story('Delete project')
@allure.title('[Project] Delete. Not existing project.')
@allure.description('Deleting not existing project should result in empty response')
@allure.tag('Regression')
@allure.severity(Severity.NORMAL)
def test_delete_not_existing_project(session):
    with allure.step(f'Delete not existing project'):
        resp = api.delete_project(session, project_id='123')
    with allure.step(f'Assert response code is 204'):
        assert resp.status_code == 204
