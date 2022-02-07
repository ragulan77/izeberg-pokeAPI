from fastapi import APIRouter, Depends, HTTPException
from .auth import AuthHandler
from .credential import Credential
from sql_app.crud import create_user, get_user_by_login
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from . import crud, models, schemas


app = APIRouter()


models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

auth_handler = AuthHandler()

@app.post('/api/register', status_code=201)
def register(auth_details: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_login(db, auth_details.login)
    if user is not None:
        raise HTTPException(status_code=400, detail='Username is taken')
    create_user(db, auth_details)
    return


@app.post('/api/login')
def login(auth_details: Credential, db: Session = Depends(get_db)):
    user = get_user_by_login()
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }