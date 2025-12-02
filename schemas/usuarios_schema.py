from pydantic import BaseModel, Field


class UsuarioCreate(BaseModel):
    username: str
    password: str = Field(min_length=8)
    id_permissao: int
    id_funcionario: int | None = None


class UsuarioUpdate(BaseModel):
    username: str | None = None
    password: str | None = None 
    id_permissao: int | None = None
    id_funcionario: int | None = None


class UsuarioResponse(BaseModel):
    id: int
    username: str
    id_permissao: int
    id_funcionario: int | None
