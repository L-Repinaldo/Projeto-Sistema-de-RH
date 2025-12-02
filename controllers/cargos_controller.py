from fastapi import APIRouter, HTTPException
from service import CargosService
from schemas import CargoCreate, CargoUpdate, CargoResponse
from typing import List

router = APIRouter(prefix="/cargos", tags=["Cargos"])
service = CargosService()

@router.post("/", response_model=CargoResponse)
def create(data: CargoCreate):
    try:
        cargo_id = service.create(nome=data.nome)
        cargo = service.get_by_id(cargo_id)
        return cargo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[CargoResponse])
def get_all():
    try:
        cargos = service.repository.get_all()
        return cargos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{cargo_id}", response_model=CargoResponse)
def get_by_id(cargo_id: int):
    try:
        cargo = service.get_by_id(cargo_id)
        return cargo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{cargo_id}", response_model=CargoResponse)
def update(cargo_id: int, data: CargoUpdate):
    try:
        service.update(cargo_id=cargo_id, nome=data.nome)
        cargo = service.get_by_id(cargo_id)
        return cargo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{cargo_id}/desactivate")
def desactivate(cargo_id: int):
    try:
        service.desactivate(cargo_id)
        return {"message": "Cargo desativado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{cargo_id}/activate")
def activate(cargo_id: int):
    try:
        service.activate(cargo_id)
        return {"message": "Cargo ativado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
