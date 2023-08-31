from pydantic import BaseModel
from typing import Optional

# Entidad user
class User(BaseModel):
    ##id: str | None        ##Deta tiene V3,9, asi que tengo que usar Optional
    id: Optional[str]
    username: str
    full_name: str
    email: str
    disable: bool
    password: str
    

class UserPublic(BaseModel):
    ##id: str | None        ##Deta tiene V3,9, asi que tengo que usar Optional
    id: Optional[str]
    username: str
    full_name: str
    email: str
    disable: bool