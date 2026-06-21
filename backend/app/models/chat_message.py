from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from app.db.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)

    user_email = Column(String, nullable=False)

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
