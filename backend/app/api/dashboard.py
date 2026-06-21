from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.jwt_security import require_admin
from app.db.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.chat_message import ChatMessage


router = APIRouter()


@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    total_users = db.query(User).count()
    total_documents = db.query(Document).count()
    total_chunks = db.query(Chunk).count()
    total_questions = db.query(ChatMessage).count()

    recent_documents = db.query(Document).order_by(
        Document.id.desc()
    ).limit(5).all()

    recent_users = db.query(User).order_by(
        User.id.desc()
    ).limit(5).all()

    return {
        "total_users": total_users,
        "total_documents": total_documents,
        "total_chunks": total_chunks,
        "total_questions": total_questions,
        "recent_documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "created_at": document.created_at
            }
            for document in recent_documents
        ],
        "recent_users": [
            {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
            for user in recent_users
        ]
    }
