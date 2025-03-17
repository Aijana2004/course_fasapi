from course_app.db.models import Lesson
from course_app.db.schema import LessonSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional,List
from fastapi import Depends,HTTPException,APIRouter


lesson_router = APIRouter(prefix='/lesson',tags=['Lessons'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@lesson_router.post('/',response_model=LessonSchema)
async def create_lesson(lesson: LessonSchema, db: Session = Depends(get_db)):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


@lesson_router.get('/',response_model=List[LessonSchema])
async def list_lesson(db: Session = Depends(get_db)):
    return db.query(Lesson).all()


@lesson_router.get('/{lesson_id}/',response_model=LessonSchema)
async def detail_lesson(lesson_id:int,db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail='lesson not found')
    return lesson


@lesson_router.put('/{lesson_id}/',response_model=LessonSchema)
async def update_lesson(lesson_id:int,lesson_data: LessonSchema,db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail='lesson not found')

    for lesson_key,lesson_value in lesson_data.dict().items():
        setattr(lesson,lesson_key,lesson_value)

    db.commit()
    db.refresh(lesson)
    return lesson


@lesson_router.delete('/{lesson_id}/')
async def delete_lesson(lesson_id:int,db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail='lesson not found')

    db.delete(lesson)
    db.commit()
    return {'message':'this lesson is deleted'}