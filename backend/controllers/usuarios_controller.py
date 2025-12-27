from fastapi import APIRouter, HTTPException, Depends
from service import UsuariosService
from schemas import  UsuarioCreate, UsuarioUpdate, UsuarioResponse
from typing import List
from pydantic import BaseModel
from utils import require_admin, log_access

class LoginRequest(BaseModel):
    username: str
    password: str



router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
service = UsuariosService()

@router.post("/", response_model = UsuarioResponse)
def create(data : UsuarioCreate, current_user: dict = Depends(require_admin)):
    try:

        user_id =  service.create(
            username = data.username,
            password = data.password,
            id_permissao = data.id_permissao,
            id_funcionario = data.id_funcionario
        )

        user = service.get_by_id(user_id)

        return user

    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))

@router.get("/", response_model=List[UsuarioResponse])
def get_all(current_user: dict = Depends(require_admin)):
    try:
        response = service.get_all()
        log_access(
            id_usuario=current_user["sub"],
            operacao="GET_USUARIOS",
            consulta="/usuarios/",
            result_count=len(response)
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_by_id(usuario_id: int, current_user: dict = Depends(require_admin)):
    try:
        user = service.get_by_id(usuario_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update(usuario_id: int, data: UsuarioUpdate, current_user: dict = Depends(require_admin)):
    try:
        updated = service.update(
            usuario_id=usuario_id,
            username=data.username,
            password=data.password,
            id_permissao=data.id_permissao,
            id_funcionario=data.id_funcionario
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        user = service.get_by_id(usuario_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{usuario_id}")
def delete(usuario_id: int, current_user: dict = Depends(require_admin)):
    try:
        deleted = service.delete(usuario_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        return {"message": "Usuario deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: LoginRequest):
    try:
        token = service.login(data.username, data.password)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




