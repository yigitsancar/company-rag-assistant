from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.chat_message import ChatMessage
from app.services.openai_service import create_embedding
from app.services.chat_service import ask_openai


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_documents(
    request: QueryRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
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

    chat_message = ChatMessage(
        user_email=user.get("sub"),
        question=request.question,
        answer=answer
    )

    db.add(chat_message)
    db.commit()

    sources = [
        {
            "chunk_id": row.id,
            "filename": row.filename,
            "page_number": row.page_number,
            "distance": float(row.distance)
        }
        for row in result
    ]

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }


@router.get("/chat/history")
def get_chat_history(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_email == user.get("sub")
    ).order_by(ChatMessage.id.desc()).limit(20).all()

    return [
        {
            "id": item.id,
            "question": item.question,
            "answer": item.answer,
            "created_at": item.created_at
        }
        for item in messages
    ]

@router.delete("/chat/history")
def delete_chat_history(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    db.query(ChatMessage).filter(
        ChatMessage.user_email == user.get("sub")
    ).delete()

    db.commit()

    return {
        "message": "Chat history deleted successfully"
    }
