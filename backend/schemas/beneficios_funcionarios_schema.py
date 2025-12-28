from pydantic import BaseModel
from typing import Optional

class BeneficioFuncionarioCreate(BaseModel):
    id_funcionario: int
    id_beneficio: int
    ativo: Optional[bool] = True

class BeneficioFuncionarioUpdate(BaseModel):
    ativo: Optional[bool] = None

class BeneficioFuncionarioResponse(BaseModel):
    id: int
    id_funcionario: int
    id_beneficio: int
    ativo: bool
