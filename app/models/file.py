import uuid
from sqlalchemy import Column, String, BigInteger, DateTime, text
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checksum = Column(String, nullable=False, unique=True)
    filename = Column(String, nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    storage_path = Column(String, nullable=False)
    schema_id = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False
    )
