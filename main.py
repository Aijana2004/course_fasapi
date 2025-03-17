import uvicorn
from course_app.db.schema import CategorySchema,CourseSchema,LessonSchema,ExamSchema,QuestionSchema,CertificateSchema,UserProfileSchema
from course_app.db.database import SessionLocal,engine
from course_app.db.models import Category,Course,Lesson,Exam,Question,Certificate,UserProfile,RefreshToken
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List,Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from congif import SEKRET_KEY,REFRESH_TOKEN_EXPIRE_DAYS,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM
from jose import jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqladmin import Admin,ModelView
from course_app.api.endpoints import auth, course, category, certificate, exam, lesson, question, cart, favorite
from course_app.admin.setup import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from course_app.congif import SEKRET_KEY

async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


course_app = FastAPI(title='Course FastAPI', lifespan=lifespan)
admin = Admin(course_app, engine)


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login/')
password_context = CryptContext(schemes=['bcrypt'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

course_app = FastAPI(title='Course FastAPI', lifespan=lifespan)
course_app.add_middleware(SessionMiddleware, secret_key="SEKRET_KEY")

setup_admin(course_app)

course_app.include_router(auth.auth_router)
course_app.include_router(category.category_router)
course_app.include_router(course.course_router)
course_app.include_router(lesson.lesson_router)
course_app.include_router(exam.exam_router)
course_app.include_router(question.question_router)
course_app.include_router(certificate.certificate_router)
course_app.include_router(cart.cart_router)
course_app.include_router(favorite.favorite_router)

if __name__ == '__main__':
    uvicorn.run(course_app, host='127.0.0.1', port=8000, workers=True)












