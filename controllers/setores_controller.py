from fastapi import APIRouter, HTTPException
from service import SetoresService
from schemas import SetorCreate, SetorUpdate, SetorResponse
from typing import List

router = APIRouter(prefix="/setores", tags=["Setores"])
service = SetoresService()

@router.post("/", response_model=SetorResponse)
def create(data: SetorCreate):
    try:
        setor_id = service.create(nome=data.nome, id_gerente=data.id_gerente)
        setor = service.repository.get_by_id(setor_id)
        return setor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[SetorResponse])
def get_all():
    try:
        setores = service.get_all()
        return setores
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{setor_id}", response_model=SetorResponse)
def get_by_id(setor_id: int):
    try:
        setor = service.repository.get_by_id(setor_id)
        if not setor:
            raise HTTPException(status_code=404, detail="Setor não encontrado")
        return setor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{setor_id}", response_model=SetorResponse)
def update(setor_id: int, data: SetorUpdate):
    try:
        service.update(id_setor=setor_id, nome=data.nome, id_gerente=data.id_gerente)
        setor = service.repository.get_by_id(setor_id)
        return setor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{setor_id}")
def delete(setor_id: int):
    try:
        service.delete(setor_id)
        return {"message": "Setor deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
