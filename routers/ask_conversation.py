from fastapi import APIRouter,Request,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from db.connection import SessionLocal
from db.models import AskConversation
from service.get_query_response import query_response

router =APIRouter()

class QueryRequest(BaseModel):
    query: str
    user_id:str
    session_id: str


@router.get("/MCP/AskConversation")
async  def get_conversation(request: QueryRequest):
    db: Session = SessionLocal()
    try:
       detail = db.query(AskConversation).filter(AskConversation.session_id == request.session_id).all()
    finally:
        db.close()
    return{"data":{"box_details":detail}}



@router.post("/MCP/AskConversation")
async def ask_conversation(request: QueryRequest):
    print("djhscbvs")
    db: Session = SessionLocal()
    print("gvhcasd")

    try:
        message_id = uuid.uuid4()
        role="user"
        message=request.query
        document_id = getattr(request, "document_id", None)
        print("step1")
        conversation = AskConversation(
            session_id=request.session_id,
            message_id=str(message_id),
            user_id=request.user_id,
            role=role,
            message=message,
            document_id=document_id
        )
        print("step2")
        db.add(conversation)
        db.commit()
        print("step3")
        response = query_response(request.query,request.session_id,request.user_id)

        sys_generated = AskConversation(
            session_id=request.session_id,
            message_id=str(response["message_sys_id"]),
            user_id=request.user_id,
            role=response["role"],
            message=response["message_sys_id"],
            document_id=response["document_id"]
        )
        db.add(sys_generated)
        db.commit()

        return JSONResponse(content={"data": {"response": response}})
    finally:
        db.close()
