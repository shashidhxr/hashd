from app.core.db import engine
from app.models.base import Base
from app.models.file import File

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()