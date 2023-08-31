from pydantic import BaseModel
from typing import Optional

# Entidad product
class Product(BaseModel):
    ##id: str | None            ##Deta tiene V3,9, asi que tengo que usar Optional
    id: Optional[str]
    name: str
    type: str
    author: str
    quantity: int
    price: int
    img: str
    deshab: Optional[bool]