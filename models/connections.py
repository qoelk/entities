from sqlalchemy import Column, Integer, ForeignKey, CHAR
from sqlalchemy.orm import relationship

from models.base import Base

class Connection(Base):
    __tablename__ = 'connections'
    head_id = Column(CHAR(32), ForeignKey('entities.id'))
    head = relationship('Entity', back_populates='head_connections', foreign_keys=[head_id])
    tail_id = Column(CHAR(32), ForeignKey('entities.id'))
    tail = relationship('Entity', back_populates='tail_connections', foreign_keys=[tail_id])
    document_id = Column(CHAR(32), ForeignKey('documents.id'))
    document = relationship('Document', back_populates='connections')

    def __repr__(self):
        return f'<Connection(id={self.id}, head_id={self.head_id}, tail_id={self.tail_id})>'