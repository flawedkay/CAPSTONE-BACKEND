from fastapi import APIRouter, Depends,HTTPException,Form,Response
from schema import SignupDetails, Token
from database import SessionLocal
from models import User
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from typing_extensions import Annotated
from datetime import timedelta, datetime
from passlib.context import CryptContext
from sqlalchemy.orm import session
from starlette import status
from jose import jwt, JWTError
from fastapi.requests import Request
from typing import Optional




auth = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#db_dependency = Annotated[session, Depends(get_db)]

SECRET_KEY = '5a9626b0b9d28e876705256960cd14299dc6a37654d8b635c191ab52aafbf6ae'

ALGORITHM = "HS256"

oauth2_bearer =  OAuth2PasswordBearer(tokenUrl="/auth/token")
bcrpyt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    
    if not bcrpyt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])    
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise None
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials")



@auth.post("/token", response_model=Token)
async def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        return False
    
    token = create_access_token(user.username, user.id, timedelta(minutes=60))
    
    return {
        "access_token": token,
        "token_type": "bearer"}








@auth.post("/signup",status_code=status.HTTP_201_CREATED)
def create_user (signup_details:SignupDetails, db: session = Depends(get_db)):
    create_user_model = User(
        email = signup_details.email,
        username = signup_details.username,
        firstname = signup_details.firstname,
        lastname = signup_details.lastname,
        hashed_password = bcrpyt_context.hash(signup_details.hashed_password)
    )

    db.add(create_user_model)
    db.commit()
    db.refresh

@auth.post("/token", response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:session=Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password, db)
    if not user:
        return "failed authentication"
    
    token = create_access_token(user.username, user.id, timedelta(minutes = 50))

    return {
        "access_token": token,
        "token_type": "bearer"
    }