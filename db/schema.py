from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from course_app.db.models import UserRole,StatusCourse,TypeCourse


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    password:str
    phone_number: Optional[str] = None
    age: Optional[int] = None
    profile_picture: Optional[str] = None
    role: str


class CategorySchema(BaseModel):
    id: int
    category_name: str


class CourseSchema(BaseModel):
    id: int
    course_name: str
    description: str
    level: str
    price: float
    type_course: str
    created_at: datetime
    updated_at: datetime
    author_id: int
    page: int
    size: int


class LessonSchema(BaseModel):
    id: int
    title: str
    video_url: Optional[str] = None
    content: Optional[str] = None
    course_id: int


class ExamSchema(BaseModel):
    id: int
    title: str
    course_id: int
    end_time: int


class QuestionSchema(BaseModel):
    id: int
    exam_id: int
    title: str
    score: int


class CertificateSchema(BaseModel):
    id: int
    student_id: int
    course_id: int
    issued_at: datetime
    certificate_url: str


class CartItemSchema(BaseModel):
    id: int
    cart_id: int
    course_id: int


class CartSchema(BaseModel):
    id: int
    user_id: int
    items: List[CartItemSchema] =[]
    total_price: float


class TestSchema(BaseModel):
    id: int
    test_name: str
    category: int


class FavoriteItemSchema(BaseModel):
    id: int
    favorite_id: int
    course_id: int


class FavoriteSchema(BaseModel):
    id: int
    user_id: int
    items_favorite: List[FavoriteItemSchema] =[]


