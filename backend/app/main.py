from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    auth_controller,
    course_controller,
    enrollment_controller,
    role_controller,
    student_controller,
    user_controller,
)
from app.models.database import close_mongo_connection, connect_to_mongo
from app.schemas.webhookSchema import WebHookPayload


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router, prefix="/api", tags=["auth"])
app.include_router(student_controller.router, prefix="/api", tags=["students"])
app.include_router(course_controller.router, prefix="/api", tags=["courses"])
app.include_router(enrollment_controller.router, prefix="/api", tags=["enrollments"])
app.include_router(role_controller.router, prefix="/api", tags=["roles"])
app.include_router(user_controller.router, prefix="/api", tags=["users"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.post("/webhook", tags=["webhook"])
async def webhook_handler(payload: WebHookPayload):
    return {"status": "received", "event": payload.event}