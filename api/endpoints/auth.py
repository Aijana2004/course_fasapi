from course_app.db.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException,APIRouter
from passlib.context import CryptContext
from course_app.congif import SEKRET_KEY,REFRESH_TOKEN_EXPIRE_DAYS,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM
from jose import jwt
from datetime import timedelta, datetime
from fastapi_limiter.depends import RateLimiter
from typing import Optional
from sqlalchemy.orm import Session
from course_app.db.models import UserProfile, RefreshToken, Cart,Favorite
from course_app.db.schema import UserProfileSchema
from starlette.requests import Request
from course_app.congif import settings,setting
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.httpx_client import OAuth1Auth

oauth = OAuth()
oauth.register(
    name='github',
    client_id=settings.CLIENT_ID_GITHUB,
    client_secret=settings.GITHUB_KEY,
    authorize_url='https://github.com/login/oauth/authorize',
)

oauth.register(
    name='google',
    client_id=setting.GOOGLE_ID_CLIENT,
    client_secret=setting.GOOGLE_KEY,
    authorize_url='https://google.com/login/oauth/authorize',
    client_kwargs = {"scope": "openid profile email"},
)


auth_router = APIRouter(prefix='/auth', tags=['Authorization'])


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login/')
password_context = CryptContext(schemes=['bcrypt'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data:dict,expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else  timedelta(microseconds=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode,SEKRET_KEY,algorithm=ALGORITHM)


def create_refresh_token(data:dict):
    return create_access_token(data,expires_delta=timedelta(days= REFRESH_TOKEN_EXPIRE_DAYS))


def verify_password(plain_password,hash_password):
    return password_context.verify(plain_password,hash_password)


def get_new_password(password):
    return password_context.hash(password)


@auth_router.post('/register/')
async def register(user:UserProfileSchema,db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if user_db:
        raise HTTPException(status_code=400, detail='username yes')
    new_hash_password = get_new_password(user.password)
    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        age=user.age,
        role=user.role,
        profile_picture=user.profile_picture,
        hashed_password=new_hash_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_cart = Cart(user_id=new_user.id)
    db.add(new_cart)
    db.commit()

    new_favorite = Favorite(user_id=new_user.id)
    db.add(new_favorite)
    db.commit()

    return {'message': ' save new user'}


@auth_router.post('/login', dependencies=[Depends(RateLimiter(times=3, seconds=200))])
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='incorrect information')
    access_token = create_access_token({'sub':user.username})
    refresh_token = create_refresh_token({'sub':user.username})

    user_db = RefreshToken(token=access_token,user_id = user.id)
    db.add(user_db)
    db.commit()

    return {'access_token':access_token,'refresh_token': refresh_token, 'token_type':'Bearer'}


@auth_router.post('/logout')
async def logout(refresh_token:str,db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        return HTTPException(status_code= 401, detail='incorrect information')
    db.delete(stored_token)
    db.commit()

    return {'massege':'logout'}


@auth_router.post('/refresh')
async def refresh(refresh_token: str,db:Session = Depends(get_db)):
    token_entry = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not token_entry:
        return HTTPException(status_code= 401, detail='incorrect information')
    access_token = create_access_token({'sub': token_entry.user_id})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@auth_router.get('/github')
async def github_login(request: Request):
    redirect_url = settings.GITHUB_LOGIN_CALLBACK
    return await oauth.github.authorize_redirect(request, redirect_url)


@auth_router.get('/google')
async def google_login(request: Request):
    redirect_url = setting.GOOGLE_LOGIN_CALLBACK
    return await oauth.google.authorize_redirect(request, redirect_url)



