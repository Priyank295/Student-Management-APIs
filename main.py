from fastapi import FastAPI
from routes.student import router as student_router

app = FastAPI()

app.include_router(student_router, prefix="/students", tags=["students"])
