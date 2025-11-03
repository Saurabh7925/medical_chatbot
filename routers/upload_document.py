from fastapi import APIRouter, Request, HTTPException, File, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uuid
from db.connection import SessionLocal
from db.models import Documents

from service.parsing_and_embeddings import split_text_into_chunks,generate_bge_embeddings

router = APIRouter()


@router.post("/MCP/upload_document/{session_id}")
async def upload_document(session_id: str,
                          user_id: str = Form(...),
                          file: UploadFile = File(...)):
    print("start")
    db: Session = SessionLocal()
    print("db initiated")
    try:
        print("step1 ")
        file_content = await file.read()
        with open(file.filename, "wb") as f:
            f.write(file_content)

        document = Documents(
            document_id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            filename=file.filename,
            file_data=file_content,
        )
        print("document uploaded ")
        chunks =split_text_into_chunks(file.filename)
        generate_bge_embeddings(chunks,session_id,user_id)

        db.add(document)
        db.commit()
        db.refresh(document)

        return {"message": "File uploaded successfully", "document_id": document.document_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
