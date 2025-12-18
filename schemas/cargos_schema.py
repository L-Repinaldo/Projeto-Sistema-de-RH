from pydantic import BaseModel
from typing import Optional

class CargoCreate(BaseModel):
    nome: str

class CargoUpdate(BaseModel):
    nome: Optional[str] = None

class CargoResponse(BaseModel):
    id: int
    nome: str
    ativo: bool
