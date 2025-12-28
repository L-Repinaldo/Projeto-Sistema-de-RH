from pydantic import BaseModel

class SetorCreate(BaseModel):
    nome: str
    id_gerente: int | None = None

class SetorUpdate(BaseModel):
    nome: str | None = None
    id_gerente: int | None = None

class SetorResponse(BaseModel):
    id: int
    nome: str
    id_gerente: int | None
