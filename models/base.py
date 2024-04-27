import uuid

from sqlalchemy import Column, String, CHAR
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

Base.id = Column(CHAR(32), primary_key=True, default=lambda: str(uuid.uuid4()))