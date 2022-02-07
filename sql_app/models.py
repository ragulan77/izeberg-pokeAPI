from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


association_table = Table('UserType', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('type_id', ForeignKey('types.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    types = relationship("Type", secondary=association_table)

class Type(Base):
    __tablename__  = "types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


