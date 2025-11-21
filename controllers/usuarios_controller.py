from fastapi import APIRouter, HTTPException, Depends
from service import UsuariosService



router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

