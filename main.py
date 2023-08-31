from fastapi import FastAPI
from routers import jwt_auth_productsdb, jwt_auth_user_db
from fastapi.middleware.cors import CORSMiddleware  ## https://fastapi.tiangolo.com/tutorial/cors/

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "https://p2.diegohcalleja.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###app.include_router(basic_users.router)       ### CRUD Usuarios sin coneccion a una BD
###app.include_router(basic_auth_user.router)   ### Ejemplo de autentificacion basica

###app.include_router(usersdb.router)           ### CRUD Usuarios con coneccion a la bd basico  
###app.include_router(usersdb_mod.router)          ### CRUD Usuarios con coneccion a la bd completo sin JWT

##app.include_router(jwt_auth_user.router)      ### Login de Usuarios con JWT sin coneccion a BD
app.include_router(jwt_auth_user_db.router)     ### Login de Usuarios con JWT con coneccion a BD

##app.include_router(productsdb.router)         ### CRUD Productos sin autentificacion
app.include_router(jwt_auth_productsdb.router)  ### CRUD Productos con autentificacion JWT

