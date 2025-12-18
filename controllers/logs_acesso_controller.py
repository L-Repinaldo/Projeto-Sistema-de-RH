from fastapi import APIRouter, HTTPException, Depends
from service import LogsAcessoService
from schemas import LogsAcessoCreate, LogsAcessoResponse
from typing import List
from datetime import datetime
from utils import require_admin

router = APIRouter(prefix="/logs_acesso", tags=["Logs Acesso"])
service = LogsAcessoService()

@router.post("/", response_model=LogsAcessoResponse)
def create(data: LogsAcessoCreate, current_user: dict = Depends(require_admin)):
    try:
        log_id = service.create(**data.dict())
        
        log = service.get_by_id(log_id)
        return log
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[LogsAcessoResponse])
def get_all(current_user: dict = Depends(require_admin)):
    try:
        return service.get_all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{log_id}", response_model=LogsAcessoResponse)
def get_by_id(log_id: int, current_user: dict = Depends(require_admin)):
    try:
        
        log = service.get_by_id(log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Log não encontrado")
        return log
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usuario/{id_usuario}", response_model=List[LogsAcessoResponse])
def get_by_usuario(id_usuario: int, current_user: dict = Depends(require_admin)):
    try:
        return service.get_by_usuario(id_usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/time_range/", response_model=List[LogsAcessoResponse])
def get_by_time_range(start_time: datetime, end_time: datetime, current_user: dict = Depends(require_admin)):
    try:
        return service.get_by_time_range(start_time, end_time)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
