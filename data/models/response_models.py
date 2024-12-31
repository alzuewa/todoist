from typing import List

import pydantic
from pydantic import BaseModel, TypeAdapter
from typing_extensions import Annotated

from data.models.request_models import Due, Duration
from data.project_constants import Color, ViewStyle


class ProjectResponse(BaseModel):
    id: str
    name: str
    comment_count: int
    order: int
    color: Color
    is_shared: bool
    is_favorite: bool
    parent_id: str | None
    is_inbox_project: bool
    is_team_inbox: bool
    view_style: ViewStyle
    url: str


class AllProjectsResponse:

    @staticmethod
    def model_validate(response):
        all_projects_response = TypeAdapter(List[ProjectResponse])
        return all_projects_response.validate_python(response)


class TaskResponse(BaseModel):
    creator_id: str
    created_at: str
    assignee_id: str | None = None
    assigner_id: str | None = None
    comment_count: int
    is_completed: bool
    content: str
    description: str
    due: Due | None = None
    duration: Duration | None = None
    id: str
    labels: List[str] | List = List
    order: Annotated[int, pydantic.Field(gt=0)]
    priority: Annotated[int, pydantic.Field(ge=1), pydantic.Field(le=4)]
    project_id: str
    section_id: str | None = None
    parent_id: str | None = None
    url: str


class AllTasksResponse:

    @staticmethod
    def model_validate(response):
        all_tasks_response = TypeAdapter(List[TaskResponse])
        return all_tasks_response.validate_python(response)
