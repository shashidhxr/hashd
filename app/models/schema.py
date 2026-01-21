from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP
from sqlalchemy.sql import func
from app.core.db import Base
import uuid

class Schema(Base):
    __tablename__ = "schemas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    schema_json = Column(JSON, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
