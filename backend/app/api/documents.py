import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_admin, require_manager_or_admin
from app.db.database import get_db
from app.models.document import Document
from app.models.chunk import Chunk
from app.services.pdf_service import extract_pages_from_pdf
from app.services.openai_service import create_embedding


router = APIRouter()

UPLOAD_DIR = "uploads"


def split_text(text: str, chunk_size: int = 400, overlap: int = 80):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


@router.get("/documents")
def list_documents(
    db: Session = Depends(get_db),
    user: dict = Depends(require_manager_or_admin)
):
    documents = db.query(Document).order_by(Document.id.desc()).all()

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "created_at": document.created_at
        }
        for document in documents
    ]


@router.post("/documents/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(require_manager_or_admin)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = Document(filename=file.filename)
    db.add(document)
    db.commit()
    db.refresh(document)

    pages = extract_pages_from_pdf(file_path)

    total_chunks = 0

    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]

        chunks = split_text(page_text)

        for chunk_text in chunks:
            embedding = create_embedding(chunk_text)

            chunk = Chunk(
                document_id=document.id,
                page_number=page_number,
                content=chunk_text,
                embedding=embedding
            )

            db.add(chunk)
            total_chunks += 1

    db.commit()

    return {
        "message": "Document uploaded successfully",
        "document_id": document.id,
        "filename": document.filename,
        "chunk_count": total_chunks
    }


@router.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(require_admin)
):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Belge bulunamadı."
        )

    db.query(Chunk).filter(Chunk.document_id == document_id).delete()
    db.delete(document)
    db.commit()

    file_path = os.path.join(UPLOAD_DIR, document.filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }
