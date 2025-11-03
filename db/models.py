from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, BLOB, Boolean, BigInteger,func,JSON,Enum
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import declarative_base
import enum
Base = declarative_base()


class RoleEnum(str, enum.Enum):
    user = "user"
    system = "system"
    assistant = "assistant"


class AskConversation(Base):
    __tablename__ = "conversations"

    message_id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-increment PK
    session_id = Column(String(50), nullable=False)# Session ID
    document_id = Column(String(50), nullable=True)
    user_id = Column(String(50), nullable=False)  # User ID
    role = Column(Enum(RoleEnum, name="role_enum"), nullable=False)  # Role enum
    message = Column(Text, nullable=False)  # Message content
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())  # Created timestamp

class Documents(Base):
    __tablename__ = "documents"

    document_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), nullable=False)
    session_id = Column(String(50), nullable=False)
    filename = Column(String(255))
    file_data = Column(BLOB, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())





