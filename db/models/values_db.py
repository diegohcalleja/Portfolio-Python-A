from pydantic import BaseModel
from typing import Optional

# Entidad values
class Value(BaseModel):
    ##id: str | None            ##Deta tiene V3,9, asi que tengo que usar Optional
    id: Optional[str]
    max_value: int
    actual_value: int
