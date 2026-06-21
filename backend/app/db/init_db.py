from app.db.database import Base, engine

from app.models.document import Document
from app.models.chunk import Chunk
from app.models.user import User
from app.models.chat_message import ChatMessage


Base.metadata.create_all(bind=engine)

print("Database initialized.")
