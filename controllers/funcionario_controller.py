from fastapi import APIRouter, HTTPException
from service import FuncionariosService
from schemas import FuncionarioCreate, FuncionarioUpdate, FuncionarioResponse
from typing import List

router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])
service = FuncionariosService()

@router.post("/", response_model=FuncionarioResponse)
def create(data: FuncionarioCreate):
    try:
        funcionario_id = service.create(**data.dict())
        funcionario = service.get_by_id(funcionario_id)
        return funcionario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[FuncionarioResponse])
def get_all():
    try:
        return service.get_all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{funcionario_id}", response_model=FuncionarioResponse)
def get_by_id(funcionario_id: int):
    try:
        return service.get_by_id(funcionario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{funcionario_id}", response_model=FuncionarioResponse)
def update(funcionario_id: int, data: FuncionarioUpdate):
    try:
        service.update(funcionario_id, **data.dict(exclude_unset=True))
        return service.get_by_id(funcionario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{funcionario_id}")
def delete(funcionario_id: int):
    try:
        service.delete(funcionario_id)
        return {"message": "Funcionário deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nome/{nome}", response_model=List[FuncionarioResponse])
def get_by_nome(nome: str):
    try:
        return service.get_by_nome(nome)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sobrenome/{sobrenome}", response_model=List[FuncionarioResponse])
def get_by_sobrenome(sobrenome: str):
    try:
        return service.get_by_sobrenome(sobrenome)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/setor/{id_setor}", response_model=List[FuncionarioResponse])
def get_by_setor(id_setor: int):
    try:
        return service.get_by_setor(id_setor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/cargo/{id_cargo}", response_model=List[FuncionarioResponse])
def get_by_cargo(id_cargo: int):
    try:
        return service.get_by_cargo(id_cargo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
