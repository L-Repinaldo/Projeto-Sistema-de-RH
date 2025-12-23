from pydantic import BaseModel
from datetime import date
from typing import Optional

class AvaliacoesCreate(BaseModel):
    id_funcionario: int
    data_avaliacao: date
    nota: float

class AvaliacoesUpdate(BaseModel):
    id_funcionario: Optional[int] = None
    nota: Optional[float] = None

class AvaliacoesResponse(BaseModel):
    id: int
    id_funcionario: int
    data_avaliacao: date
    nota: float
