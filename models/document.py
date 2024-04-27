from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship

from models.base import Base


class Document(Base):
    __tablename__ = 'documents'
    name = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    document_date = Column(Date, nullable=True)
    entities = relationship('Entity', )
    connections = relationship('Connection', )

    def __repr__(self):
        return f'<Document(id={self.id}, name={self.name}, document_date={self.document_date})>'
