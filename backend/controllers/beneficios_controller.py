from fastapi import APIRouter, HTTPException, Depends
from service import BeneficiosService
from schemas import BeneficioCreate, BeneficioUpdate, BeneficioResponse
from typing import List
from utils import require_rh_or_admin, require_user_or_higher

router = APIRouter(prefix="/beneficios", tags=["Beneficios"])
service = BeneficiosService()

@router.post("/", response_model=BeneficioResponse)
def create(data: BeneficioCreate, current_user: dict = Depends(require_rh_or_admin)):
    try:
        beneficio_id = service.create(nome=data.nome)
        beneficio = service.get_by_id(beneficio_id)
        return beneficio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[BeneficioResponse])
def get_all(current_user: dict = Depends(require_user_or_higher)):
    try:
        beneficios = service.get_all()
        return beneficios
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{beneficio_id}", response_model=BeneficioResponse)
def get_by_id(beneficio_id: int, current_user: dict = Depends(require_user_or_higher)):
    try:
        beneficio = service.get_by_id(beneficio_id)
        return beneficio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{beneficio_id}", response_model=BeneficioResponse)
def update(beneficio_id: int, data: BeneficioUpdate, current_user: dict = Depends(require_rh_or_admin)):
    try:
        service.repository.update(id_beneficios=beneficio_id, nome=data.nome)
        beneficio = service.get_by_id(beneficio_id)
        return beneficio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{beneficio_id}")
def delete(beneficio_id: int, current_user: dict = Depends(require_rh_or_admin)):
    try:
        service.delete(beneficio_id)
        return {"message": "Beneficio deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
