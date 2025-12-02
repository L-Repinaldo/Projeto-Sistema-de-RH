from pydantic import BaseModel
from typing import Optional

class BeneficioCreate(BaseModel):
    nome: str

class BeneficioUpdate(BaseModel):
    nome: Optional[str] = None

class BeneficioResponse(BaseModel):
    id: int
    nome: str
