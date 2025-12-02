from fastapi import APIRouter, HTTPException
from service import BeneficiosService
from schemas import BeneficioCreate, BeneficioUpdate, BeneficioResponse
from typing import List

router = APIRouter(prefix="/beneficios", tags=["Beneficios"])
service = BeneficiosService()

@router.post("/", response_model=BeneficioResponse)
def create(data: BeneficioCreate):
    try:
        beneficio_id = service.create(nome=data.nome)
        beneficio = service.get_by_id(beneficio_id)
        return beneficio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[BeneficioResponse])
def get_all():
    try:
        beneficios = service.get_all()
        return beneficios
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{beneficio_id}", response_model=BeneficioResponse)
def get_by_id(beneficio_id: int):
    try:
        beneficio = service.get_by_id(beneficio_id)
        return beneficio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{beneficio_id}", response_model=BeneficioResponse)
def update(beneficio_id: int, data: BeneficioUpdate):
    try:
        service.repository.update(id_beneficios=beneficio_id, nome=data.nome)
        beneficio = service.get_by_id(beneficio_id)
        return beneficio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{beneficio_id}")
def delete(beneficio_id: int):
    try:
        service.delete(beneficio_id)
        return {"message": "Beneficio deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
