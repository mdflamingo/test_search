import uuid
from dataclasses import dataclass, field
from pydantic import BaseModel


@dataclass
class PostPG:
    rubrics: str
    text: str
    created_date: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


class PostES(BaseModel):
    id: str
    text: str
