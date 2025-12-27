from fastapi import APIRouter, HTTPException, Depends
from service import CargosService
from schemas import CargoCreate, CargoUpdate, CargoResponse
from typing import List
from utils import require_rh_or_admin, require_user_or_higher, log_access


router = APIRouter(prefix="/cargos", tags=["Cargos"])
service = CargosService()

@router.post("/", response_model=CargoResponse)
def create(data: CargoCreate, current_user: dict = Depends(require_rh_or_admin)):
    try:
        cargo_id = service.create(nome=data.nome)
        cargo = service.get_by_id(cargo_id)
        return cargo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[CargoResponse])
def get_all(current_user: dict = Depends(require_user_or_higher)):
    try:
        response = service.repository.get_all()
        log_access(
            id_usuario=current_user["sub"],
            operacao="GET_CARGOS",
            consulta="/cargos/",
            result_count=len(response)
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{cargo_id}", response_model=CargoResponse)
def get_by_id(cargo_id: int, current_user: dict = Depends(require_user_or_higher)):
    try:
        cargo = service.get_by_id(cargo_id)
        return cargo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{cargo_id}", response_model=CargoResponse)
def update(cargo_id: int, data: CargoUpdate, current_user: dict = Depends(require_rh_or_admin)):
    try:
        service.update(cargo_id=cargo_id, nome=data.nome)
        cargo = service.get_by_id(cargo_id)
        return cargo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{cargo_id}/desactivate")
def desactivate(cargo_id: int, current_user: dict = Depends(require_rh_or_admin)):
    try:
        service.desactivate(cargo_id)
        return {"message": "Cargo desativado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{cargo_id}/activate")
def activate(cargo_id: int, current_user: dict = Depends(require_rh_or_admin)):
    try:
        service.activate(cargo_id)
        return {"message": "Cargo ativado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
