from pydantic_settings import BaseSettings

from utils.env_path_getter import get_resource_path


class Config(BaseSettings):
    base_url: str = 'https://api.todoist.com/rest/v2'
    token: str
    inbox_id: str


config = Config(_env_file=get_resource_path('.env'))
