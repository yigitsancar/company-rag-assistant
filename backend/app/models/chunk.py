from sqlalchemy import Column, Integer, ForeignKey, Text
from pgvector.sqlalchemy import Vector

from app.db.database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    page_number = Column(Integer)

    content = Column(Text, nullable=False)

    embedding = Column(Vector(1536))
