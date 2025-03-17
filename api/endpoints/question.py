from course_app.db.models import Question
from course_app.db.schema import QuestionSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional,List
from fastapi import Depends,HTTPException,APIRouter


question_router = APIRouter(prefix='/question',tags=['Questions'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@question_router.post('/',response_model=QuestionSchema)
async def create_question(question: QuestionSchema, db: Session = Depends(get_db)):
    db_question= Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@question_router.get('/',response_model=List[QuestionSchema])
async def list_question(db: Session = Depends(get_db)):
    return db.query(Question).all()


@question_router.get('/{question_id}/',response_model=QuestionSchema)
async def detail_question(question_id:int,db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='question not found')
    return question


@question_router.put('/{question_id}/',response_model=QuestionSchema)
async def update_question(question_id:int,question_data: QuestionSchema,db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='question not found')

    for question_key,question_value in question_data.dict().items():
        setattr(question,question_key,question_value)

    db.commit()
    db.refresh(question)
    return question


@question_router.delete('/{question_id}/')
async def delete_question(question_id:int,db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='question not found')

    db.delete(question)
    db.commit()
    return {'message':'this question is deleted'}
