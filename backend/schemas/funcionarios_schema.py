from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class FuncionarioCreate(BaseModel):
    nome: str
    sobrenome: str
    cpf: str
    email: str
    id_setor: int
    id_cargo: int
    salario: float
    data_nascimento: date
    data_admissao: date

class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[str] = None
    id_setor: Optional[int] = None
    id_cargo: Optional[int] = None
    salario: Optional[float] = None

class FuncionarioResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    cpf: str
    email: str
    id_setor: int
    id_cargo: int
    salario: float
    data_nascimento: date
    data_admissao: date
