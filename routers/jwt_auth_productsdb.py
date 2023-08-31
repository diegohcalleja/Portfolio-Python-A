from fastapi import APIRouter, HTTPException, status, Depends

from db.models.product import Product
from db.models.values_db import Value

from db.client import db_client

from db.schemas.product import product_schema, products_schema
from db.schemas.values import value_schema, values_schema

from bson import ObjectId
from typing import Optional

from routers.jwt_auth_user_db import auth_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

from db.secret_const.secret_const import ALGORITHM,ACCESS_TOKEN_DURATION,SECRET, ID_VALUES


oauth2 = OAuth2PasswordBearer(tokenUrl="/")

delete_id = ""

router = APIRouter(prefix="/productsdb",tags={"Products"}, responses={status.HTTP_404_NOT_FOUND:{"Error": "No encontrado"}})

 ##################################
 ###            GET             ###
 ##################################

@router.get("/",status_code=status.HTTP_200_OK)
##async def product_byquery(name:str|None = None, type: str|None = None, author: str|None = None):     ##Deta tiene V3,9, asi que tengo que usar Optional
async def product_byquery(name:Optional[str] = None, type: Optional[str] = None, author: Optional[str] = None): 
   return search_product(name, type, author)


##def search_product (name:str|None = None, type: str|None = None, author: str|None = None):            ##Deta tiene V3,9, asi que tengo que usar Optional
def search_product (name:Optional[str] = None, type: Optional[str] = None, author: Optional[str] = None):
    try:
        flag = None

        if not name and not type and not author:
            return products_schema(db_client.products.find())
            
        else:
            if name:
                products = products_schema(db_client.products.find({'name':{'$regex':''.join(["^",name])}}))
                if (products):
                    return products
                else:
                    raise HTTPException(status.HTTP_204_NO_CONTENT, detail='Error: No hay productos')
                
            elif type:
                products = products_schema(db_client.products.find({'type':{'$regex':''.join(["^",type])}}))
                if (products):
                    return products
                else:
                    raise HTTPException(status.HTTP_204_NO_CONTENT, detail='Error: No hay productos')

            elif author:
                products = products_schema(db_client.products.find({'author':{'$regex':''.join(["^",author])}}))
                if (products):
                    return products
                else:
                    raise HTTPException(status.HTTP_204_NO_CONTENT, detail='Error: No hay productos')

    except:
        raise HTTPException(status.HTTP_204_NO_CONTENT, detail='Error: No hay productos')

 ##################################
 ###            POST            ###
 ##################################

async def product_post_jwt (product:Product,token: str = Depends(oauth2)):

    exception_a = HTTPException(status.HTTP_401_UNAUTHORIZED,
            detail="Error: Fallo de autenticacion / token expirado", 
            headers={"WWW-Authenticate":"bearer"}) 
    
    exception_b = HTTPException(status.HTTP_401_UNAUTHORIZED,
             detail="Error: Usuario deshabilitado")

    try:
        username = jwt.decode(token,SECRET,algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception_a
      
        value = value_schema(db_client.values_db.find_one({"_id":ObjectId(ID_VALUES)}))

        if value["actual_value"] < value["max_value"]:

            product_dict = dict(product)
            del product_dict["id"]

            del product_dict["deshab"]
            product_dict["deshab"] = False

            if type(product_dict["name"])==str and  type(product_dict["type"])==str and type(product_dict["author"])==str and type(product_dict["quantity"])==int and type(product_dict["price"])==int and type(product_dict["img"])==str and type(product_dict["deshab"])==bool:

                id = db_client.products.insert_one(product_dict).inserted_id
                new_product = product_schema(db_client.products.find_one({"_id":id}))

                value["actual_value"] += 1
                try:
                    db_client.values_db.find_one_and_replace({"_id":ObjectId(ID_VALUES)},value)
                except:
                    raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail='Error: No se ha actualizado la tabla de valores')

                return Product(**new_product)
            
            else:

                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail='Error: Error de ingreso')
            
        else:

            raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail='Error: Maximo numero de articulos alcanzado')

    except JWTError:
       raise exception_a



@router.post("/",response_model=Product, status_code=status.HTTP_201_CREATED)
async def product_post(product: Product = Depends(product_post_jwt)):
    return product

##################################
###            DELETE          ###
##################################

async def product_delete_jwt (id:str,token: str = Depends(oauth2)):

    exception_a = HTTPException(status.HTTP_401_UNAUTHORIZED,
             detail="Error: Fallo de autenticacion / token expirado", 
             headers={"WWW-Authenticate":"bearer"}) 
    
    exception_b = HTTPException(status.HTTP_401_UNAUTHORIZED,
             detail="Error: Usuario deshabilitado")

    try:
        username = jwt.decode(token,SECRET,algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception_a
      
        value = value_schema(db_client.values_db.find_one({"_id":ObjectId(ID_VALUES)}))

        try:
            product = product_schema(db_client.products.find_one({"_id":ObjectId(id)}))
            
            if not product["deshab"]:                                                           ## Si es true, se puede borrar

                found = db_client.products.find_one_and_delete({"_id":ObjectId(id)})

                if found:

                    value["actual_value"] -= 1
                    try:
                        db_client.values_db.find_one_and_replace({"_id":ObjectId(ID_VALUES)},value)
                    except:
                        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail='Error: No se ha actualizado la tabla de valores')

                    return {"OK":"Articulo eliminado"}
                else:
                    raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail='Error: El articulo no se elimino')
                
            else:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= "Error: Articulo incluido de forma permanente")
            
        except:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail= "Error: Try error")

    except JWTError:
       raise exception_a
    
@router.delete("/{id}",status_code = status.HTTP_200_OK)
async def product_delete (result:str = Depends(product_delete_jwt)):
    return result

##################################
###            PUT             ###
##################################

async def product_put_jwt (product:Product,token: str = Depends(oauth2)):

    exception_a = HTTPException(status.HTTP_401_UNAUTHORIZED,
             detail="Error: Fallo de autenticacion / token expirado", 
             headers={"WWW-Authenticate":"bearer"}) 
    
    exception_b = HTTPException(status.HTTP_401_UNAUTHORIZED,
             detail="Error: Usuario deshabilitado")

    try:
        username = jwt.decode(token,SECRET,algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception_a
      
        product_dict = dict(product)
        del product_dict["id"]

        try:
            db_client.products.find_one_and_replace({"_id":ObjectId(product.id)},product_dict)

        except:
            return {"Error":"No se ha actualizado el producto"}
        
        return search_product_byid("_id",ObjectId(product.id))

    except JWTError:
       raise exception_a


def search_product_byid (field: str, key: ObjectId):
    try:
        product = product_schema (db_client.products.find_one({field:key}))
        return Product(**product)
    except:
        return {"Error":"Producto no encontrado"}


@router.put("/",response_model=Product,status_code = status.HTTP_200_OK)
async def product_put (product:Product = Depends(product_put_jwt)):
    return product

##################################
###       GET VALUES DB        ###
##################################

@router.get("/values",status_code=status.HTTP_200_OK)       ##  Obtiene toda la bd
async def values_get ():
    value = value_schema(db_client.values_db.find_one({"_id":ObjectId(ID_VALUES)}))
    return Value(**value)

def search_values():
    return values_schema(db_client.values_db.find())