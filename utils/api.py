from typing import Optional

from data.models.request_models import ProjectRequest, TaskRequest
from .session import ApiSession


def create_project(session: ApiSession, json: Optional[ProjectRequest] = None):
    if json:
        json = json.model_dump(exclude_unset=True)
        with session:
            response = session.post('/projects', json=json)
    else:
        response = session.post('/projects')
    return response


def get_project(session: ApiSession, project_id: str):
    response = session.get(f'/projects/{project_id}')
    return response


def get_all_projects(session: ApiSession):
    response = session.get('/projects')
    return response


def update_project(session: ApiSession, project_id: str, json: Optional[ProjectRequest] = None):
    if json:
        json = json.model_dump(exclude_unset=True)
        with session:
            response = session.post(f'/projects/{project_id}', json=json)
    else:
        response = session.post(f'/projects/{project_id}')
    return response


def delete_project(session: ApiSession, project_id: str):
    with session:
        response = session.delete(f'/projects/{project_id}')
    return response


def create_task(session: ApiSession, json: Optional[TaskRequest] = None):
    if json:
        json = json.model_dump(exclude_unset=True)
        with session:
            response = session.post('/tasks', json=json)
    else:
        response = session.post('/tasks')
    return response


def get_all_tasks(session: ApiSession):
    response = session.get('/tasks')
    return response


def get_task(session: ApiSession, task_id: str):
    response = session.get(f'/tasks/{task_id}')
    return response


def delete_task(session: ApiSession, task_id: str):
    with session:
        response = session.delete(f'/tasks/{task_id}')
    return response


def update_task(session: ApiSession, task_id: str, json: Optional[TaskRequest] = None):
    if json:
        json = json.model_dump(exclude_unset=True)
        with session:
            response = session.post(f'/tasks/{task_id}', json=json)
    else:
        response = session.post(f'/tasks/{task_id}')
    return response


def close_task(session: ApiSession, task_id: str):
    response = session.post(f'/tasks/{task_id}/close')
    return response
