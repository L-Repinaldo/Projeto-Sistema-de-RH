from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogsAcessoCreate(BaseModel):
    id_usuario: int
    operacao: str
    consulta: str
    result_count: Optional[int] = None
    time_stamp: Optional[datetime] = None

class LogsAcessoResponse(BaseModel):
    id: int
    id_usuario: int
    operacao: Optional[str] = None
    consulta: Optional[str] = None
    result_count: Optional[int] = None
    time_stamp: datetime
