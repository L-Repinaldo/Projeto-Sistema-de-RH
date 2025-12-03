from fastapi import APIRouter, HTTPException, Depends
from service import FuncionariosService
from schemas import FuncionarioCreate, FuncionarioUpdate, FuncionarioResponse
from typing import List
from utils import require_rh_or_admin, require_user_or_higher

router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])
service = FuncionariosService()

@router.post("/", response_model=FuncionarioResponse)
def create(data: FuncionarioCreate, current_user: dict = Depends(require_rh_or_admin)):
    try:
        funcionario_id = service.create(**data.dict())
        funcionario = service.get_by_id(funcionario_id)
        return funcionario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[FuncionarioResponse])
def get_all(current_user: dict = Depends(require_rh_or_admin)):
    try:
        return service.get_all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{funcionario_id}", response_model=FuncionarioResponse)
def get_by_id(funcionario_id: int, current_user: dict = Depends(require_user_or_higher)):
    try:
        return service.get_by_id(funcionario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{funcionario_id}", response_model=FuncionarioResponse)
def update(funcionario_id: int, data: FuncionarioUpdate, current_user: dict = Depends(require_rh_or_admin)):
    try:
        service.update(funcionario_id, **data.dict(exclude_unset=True))
        return service.get_by_id(funcionario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{funcionario_id}")
def delete(funcionario_id: int, current_user: dict = Depends(require_rh_or_admin)):
    try:
        service.delete(funcionario_id)
        return {"message": "Funcionário deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nome/{nome}", response_model=List[FuncionarioResponse])
def get_by_nome(nome: str, current_user: dict = Depends(require_user_or_higher)):
    try:
        return service.get_by_nome(nome)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sobrenome/{sobrenome}", response_model=List[FuncionarioResponse])
def get_by_sobrenome(sobrenome: str, current_user: dict = Depends(require_user_or_higher)):
    try:
        return service.get_by_sobrenome(sobrenome)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/setor/{id_setor}", response_model=List[FuncionarioResponse])
def get_by_setor(id_setor: int, current_user: dict = Depends(require_user_or_higher)):
    try:
        return service.get_by_setor(id_setor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/cargo/{id_cargo}", response_model=List[FuncionarioResponse])
def get_by_cargo(id_cargo: int, current_user: dict = Depends(require_user_or_higher)):
    try:
        return service.get_by_cargo(id_cargo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
