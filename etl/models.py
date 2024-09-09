import uuid

from pydantic import BaseModel, Field


class Post(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    rubrics: str
    text: str
    created_date: str
