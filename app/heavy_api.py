from typing import List

import requests
from pydantic import BaseModel

BASE_URL = "https://api.hevyapp.com/v1"


class ExerciseTemplate(BaseModel):
    id: str
    title: str
    type: str
    primary_muscle_group: str
    secondary_muscle_groups: List[str]
    is_custom: bool


class ExerciseTemplatesResponse(BaseModel):
    page: int
    page_count: int
    exercise_templates: List[ExerciseTemplate]


def get_exercise_templates(api_key: str, page=1, page_size=5) -> ExerciseTemplatesResponse:
    """
    Fetch exercise templates from the Hevy API.

    Args:
        page (int): The page number to fetch.
        page_size (int): The number of items per page.
        api_key (str): The API key for authentication.

    Returns:
        dict: The API response as a JSON object.
    """
    url = f"{BASE_URL}/exercise_templates?page={page}&pageSize={page_size}"
    headers = {"accept": "application/json", "api-key": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return ExerciseTemplatesResponse(**response.json())
    else:
        response.raise_for_status()
        raise Exception("An error occurred.")
