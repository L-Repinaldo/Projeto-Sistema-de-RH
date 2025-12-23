from pydantic import BaseModel
from typing import Optional

class PermissaoCreate(BaseModel):
    nome: str

class PermissaoUpdate(BaseModel):
    nome: Optional[str] = None

class PermissaoResponse(BaseModel):
    id: int
    nome: str
    ativo: bool
