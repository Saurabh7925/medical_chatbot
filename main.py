
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.ask_conversation import router as ask_conversation
from routers.upload_document import router as upload_document


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask_conversation)
app.include_router(upload_document)
