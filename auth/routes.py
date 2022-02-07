from fastapi import APIRouter, Depends, HTTPException
from .auth import AuthHandler
from .credential import Credential
from sql_app.crud import create_user, get_user_by_login
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.schemas import UserBase, UserCreate


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
    user = get_user_by_login(db, auth_details.login)
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.hashed_password)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    ub = UserBase(login=user.login, first_name=user.first_name, last_name=user.last_name, types=user.types)
    token = auth_handler.encode_token(ub)
    return { 'token': token }


@app.get('/api/user/me')
def me(token=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    print(token)
    return get_user_by_login(db, token['login'])