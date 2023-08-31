from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from db.client import db_client
from db.schemas.user import user_schema, user_schema_public
from db.models.user import UserPublic

from db.secret_const.secret_const import ALGORITHM,ACCESS_TOKEN_DURATION,SECRET

router = APIRouter(tags={"Users"})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes="bcrypt")


async def auth_user(token: str = Depends(oauth2)):

    exception_a = HTTPException(status.HTTP_401_UNAUTHORIZED,
             detail="Error: Fallo de autenticacion / token expirado", 
             headers={"WWW-Authenticate":"bearer"}) 
    
    exception_b = HTTPException(status.HTTP_401_UNAUTHORIZED,
             detail="Error: Usuario deshabilitado")

    try:
        username = jwt.decode(token,SECRET,algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception_a
      
        ##return search_user(username)
        actual_user = user_schema_public(db_client.users.find_one({'username':username}))

        if actual_user["disable"]==True: 
            raise exception_b
        else:
            return actual_user

    except JWTError:
       raise exception_a

##################################
###       POST: LOGIN          ###
##################################

@router.post("/login")
async def login (form: OAuth2PasswordRequestForm = Depends()):

    primar_user = db_client.users.find_one({'username':form.username})  ## No aplico el user_schema_public, sino da error 
                                                                        ## al ingresar un usuario incorrecto
    if not primar_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Error: Usuario / password incorrectos")

    ##user_db = user_schema_public(primar_user)
    ##if not user_db:
    ##    raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Error: Usuario incorrectos")

    user = user_schema(db_client.users.find_one({'username':form.username}))
    if not crypt.verify(form.password,user["password"]):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Error: Usuario / password incorrectos")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": user["username"], "exp": expire}
    
    return {"access_token": jwt.encode(access_token,SECRET,algorithm=ALGORITHM), "token_type": "bearer"}

##################################
###       GET: ACT. USER       ###
##################################

@router.get("/users/me")
async def me(user: UserPublic = Depends(auth_user)):
    return user

