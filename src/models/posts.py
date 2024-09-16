import uuid

from db.postgres import Base
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID


class Post(Base):
    __tablename__ = 'posts'
    __table_args = {'extend_exissting': True}

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, primary_key=True)
    rubrics = Column(String(255), nullable=False)
    created_date = Column(String(255), nullable=True)
    text = Column(Text)
