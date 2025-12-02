from fastapi import APIRouter, HTTPException
from service import BeneficiosFuncionariosService
from schemas import BeneficioFuncionarioCreate, BeneficioFuncionarioUpdate, BeneficioFuncionarioResponse
from typing import List

router = APIRouter(prefix="/beneficios-funcionarios", tags=["BeneficiosFuncionarios"])
service = BeneficiosFuncionariosService()

@router.post("/", response_model=BeneficioFuncionarioResponse)
def create(data: BeneficioFuncionarioCreate):
    try:
        beneficio_funcionario_id = service.create(funcionario_id=data.id_funcionario, beneficio_id=data.id_beneficio, ativo=data.ativo)
        beneficio_funcionario = service.repository.get_by_id(beneficio_funcionario_id)
        return beneficio_funcionario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[BeneficioFuncionarioResponse])
def get_all():
    try:
        beneficios_funcionarios = service.get_all()
        return beneficios_funcionarios
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{beneficio_funcionario_id}", response_model=BeneficioFuncionarioResponse)
def get_by_id(beneficio_funcionario_id: int):
    try:
        beneficio_funcionario = service.repository.get_by_id(beneficio_funcionario_id)
        if not beneficio_funcionario:
            raise HTTPException(status_code=404, detail="BeneficioFuncionario não encontrado")
        return beneficio_funcionario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{beneficio_funcionario_id}", response_model=BeneficioFuncionarioResponse)
def update(beneficio_funcionario_id: int, data: BeneficioFuncionarioUpdate):
    try:
        service.update(id_beneficio_funcionario=beneficio_funcionario_id, ativo=data.ativo)
        beneficio_funcionario = service.repository.get_by_id(beneficio_funcionario_id)
        return beneficio_funcionario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{beneficio_funcionario_id}")
def delete(beneficio_funcionario_id: int):
    try:
        service.delete(beneficio_funcionario_id)
        return {"message": "BeneficioFuncionario deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
