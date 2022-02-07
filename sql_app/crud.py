from sqlalchemy.orm import Session
from auth.auth import AuthHandler

from . import models, schemas

auth_handler = AuthHandler()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()



def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth_handler.get_password_hash(user.password)
    db_user = models.User(
        login=user.login,
        first_name=user.first_name,
        last_name=user.last_name,
        types=user.types,
        hashed_password=hashed_password
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_type_to_user(db: Session, type: schemas.TypeBase, user_login: str):
    print(type)
    db_type = db.query(models.Type).filter(models.Type.name == type.name).first()
    if db_type is None:
        db_type = models.Type(name=type.name)
        db.add(db_type)
        db.commit()
        db.refresh(db_type)
    db_user = db.query(models.User).filter(models.User.login == user_login).one()
    db_user.types.append(db_type)
    db.commit()

    