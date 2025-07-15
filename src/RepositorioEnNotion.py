from typing import Annotated
from pydantic import BaseModel, Secret
from pydantic.types import StringConstraints

ClaveNoVacia = Secret[Annotated[str, StringConstraints(min_length=8)]]


class RepositorioEnNotion(BaseModel):
    notion_api_key: ClaveNoVacia
    database_id: ClaveNoVacia
