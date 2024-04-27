from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from starlette.middleware.cors import CORSMiddleware

from models.base import Base
from models.document import Document
from models.entity import Entity
from models.connections import Connection

SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_document(db, document_id):
    document = db.query(Document).filter(Document.id == document_id).first()
    return document


def get_graph(db, document_id):
    entities = db.query(Entity).filter(Entity.document_id == document_id).all()
    connections = db.query(Connection).filter(Connection.document_id == document_id).all()
    nodes = [{"id": entity.id, "name": entity.data} for entity in entities]
    links = [{"source": connection.head_id, "target": connection.tail_id} for connection in connections]
    return nodes, links


@app.get("/documents/{document_id}")
def read_document(document_id: str, db: Session = Depends(get_db)):
    document = get_document(db, document_id)
    return {"document": document}


@app.get("/documents/{document_id}/graph")
def read_graph(document_id: str, db: Session = Depends(get_db)):
    nodes, links = get_graph(db, document_id)
    return {"nodes": nodes, "links": links}


@app.get("/documents")
def read_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return {"documents": documents}
