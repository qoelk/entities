from sqlalchemy import Integer, Column, String, ForeignKey, CHAR
from sqlalchemy.orm import relationship

from models.base import Base


class Entity(Base):
    __tablename__ = 'entities'
    data = Column(String(255), nullable=False)
    entity_type = Column(String(255), nullable=False)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)
    document_id = Column(CHAR(32), ForeignKey('documents.id'))
    document = relationship('Document', back_populates='entities')

    head_connections = relationship('Connection', foreign_keys='Connection.head_id')
    tail_connections = relationship('Connection', foreign_keys='Connection.tail_id')

    def __repr__(self):
        return f'<Entity(id={self.id}, data={self.data}, entity_type={self.entity_type}, start={self.start}, end={self.end})>'

    def set_data(self, matches):
        self.data = ' '.join([token.value for token in matches.tokens])