from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.openai_service import create_embedding
from app.services.chat_service import ask_openai


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_documents(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    question_embedding = create_embedding(request.question)

    sql = text("""
        SELECT
            chunks.id,
            chunks.content,
            chunks.page_number,
            documents.filename,
            chunks.embedding <-> CAST(:embedding AS vector) AS distance
        FROM chunks
        JOIN documents ON documents.id = chunks.document_id
        ORDER BY chunks.embedding <-> CAST(:embedding AS vector)
        LIMIT 3
    """)

    result = db.execute(
        sql,
        {
            "embedding": str(question_embedding)
        }
    ).fetchall()

    context = "\n\n".join([row.content for row in result])

    answer = ask_openai(
        question=request.question,
        context=context
    )

    sources = [
        {
            "chunk_id": row.id,
            "filename": row.filename,
            "page_number": row.page_number,
            "content": row.content,
            "distance": float(row.distance)
        }
        for row in result
    ]

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }
