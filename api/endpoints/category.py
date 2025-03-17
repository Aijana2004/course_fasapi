from course_app.db.models import Category
from course_app.db.schema import CategorySchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional,List
from fastapi import Depends,HTTPException,APIRouter


category_router = APIRouter(prefix='/category',tags=['Categories'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/',response_model=CategorySchema)
async def create_category(category: CategorySchema,db: Session = Depends(get_db)):
    db_category = Category(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@category_router.get('/',response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get('/{category_id}/',response_model=CategorySchema)
async def detail_category(category_id:int,db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='category not found')
    return category


@category_router.put('/{category_id}/',response_model=CategorySchema)
async def update_category(category_id:int,category_data: CategorySchema,db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='category not found')
    category.category_name = category_data.category_name
    db.commit()
    db.refresh(category)
    return category


@category_router.delete('/{category_id}/',response_model=CategorySchema)
async def delete_category(category_id:int,db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='category not found')
    db.delete(category)
    db.commit()
    return category