from pydantic import BaseModel


class Credential(BaseModel):
    login: str
    password: str