from fastapi import APIRouter, HTTPException
from service import AvaliacoesService
from schemas import AvaliacoesCreate, AvaliacoesResponse
from typing import List
from datetime import date

router = APIRouter(prefix="/avaliacoes", tags=["Avaliacoes"])
service = AvaliacoesService()

@router.post("/", response_model=AvaliacoesResponse)
def create(data: AvaliacoesCreate):
    try:
        avaliacao_id = service.create(**data.dict())
    
        avaliacao = service.get_by_id(avaliacao_id)
        return avaliacao
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AvaliacoesResponse])
def get_all():
    try:
        return service.get_all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{avaliacao_id}", response_model=AvaliacoesResponse)
def get_by_id(avaliacao_id: int):
    try:
    
        avaliacao = service.get_by_id(avaliacao_id)
        if not avaliacao:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        return avaliacao
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{avaliacao_id}")
def delete(avaliacao_id: int):
    try:
        service.delete(avaliacao_id)
        return {"message": "Avaliação deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/funcionario/{id_funcionario}", response_model=List[AvaliacoesResponse])
def get_by_funcionario(id_funcionario: int):
    try:
        return service.get_by_funcionario(id_funcionario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/date_range/", response_model=List[AvaliacoesResponse])
def get_by_date_range(start_date: date, end_date: date):
    try:
        return service.get_by_date_range(start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nota_range/", response_model=List[AvaliacoesResponse])
def get_by_nota_range(min_nota: float, max_nota: float):
    try:
        return service.get_by_nota_range(min_nota, max_nota)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
