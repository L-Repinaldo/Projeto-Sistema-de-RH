from fastapi import APIRouter, HTTPException
from service import PermissoesService
from schemas import PermissaoCreate, PermissaoUpdate, PermissaoResponse
from typing import List

router = APIRouter(prefix="/permissoes", tags=["Permissoes"])
service = PermissoesService()

@router.post("/", response_model=PermissaoResponse)
def create(data: PermissaoCreate):
    try:
        permissao_id = service.create(nome=data.nome)
        permissao = service.repository.get_by_id(permissao_id)
        return permissao
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PermissaoResponse])
def get_all():
    try:
        permissoes = service.get_all()
        return permissoes
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{permissao_id}", response_model=PermissaoResponse)
def get_by_id(permissao_id: int):
    try:
        permissao = service.repository.get_by_id(permissao_id)
        if not permissao:
            raise HTTPException(status_code=404, detail="Permissao não encontrada")
        return permissao
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{permissao_id}", response_model=PermissaoResponse)
def update(permissao_id: int, data: PermissaoUpdate):
    try:
        service.update(id_permissao=permissao_id, nome=data.nome)
        permissao = service.repository.get_by_id(permissao_id)
        return permissao
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{permissao_id}/desactivate")
def desactivate(permissao_id: int):
    try:
        service.desactivate(permissao_id)
        return {"message": "Permissao desativada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{permissao_id}/activate")
def activate(permissao_id: int):
    try:
        service.activate(permissao_id)
        return {"message": "Permissao ativada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
