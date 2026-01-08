from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Callable

from utils import jwt_util            
from repositories import PermissoesRepository

security = HTTPBearer(auto_error=False)


permissoes_repo = PermissoesRepository()

ADMIN_NAME = "ADMIN"
RH_NAME = "RH"
GERENTE_NAME = "GERENTE"
USER_NAME = "USER"

def _unauthorized(detail="Credenciais inválidas"):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

def _forbidden(detail="Acesso negado"):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def _get_payload_from_credentials(credentials: HTTPAuthorizationCredentials | None = Depends(security)):
    """
    Pega o token do header Authorization: Bearer <token>, decodifica e retorna o payload.
    Lança 401 se não houver token ou se invalid/expired.
    """
    if not credentials or credentials.scheme.lower() != "bearer":
        _unauthorized("Token ausente ou esquema inválido")

    token = credentials.credentials
    payload = jwt_util.verify_token(token)
    if payload is None:
        _unauthorized("Token inválido ou expirado")
    return payload


def _check_perm_by_id(id_permissao: int):
    """
    Retorna o registro da permissao (row) ou None.
    """
    return permissoes_repo.get_by_id(id_permissao)


def _require_permission(allowed_names: list[str], credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Helper function to require specific permissions.
    Raises 403 if permission not allowed.
    """
    payload = _get_payload_from_credentials(credentials)
    id_perm = payload.get("id_permissao")
    if id_perm is None:
        _forbidden("Permissão ausente no token")

    perm = _check_perm_by_id(id_perm)
    if not perm or not perm.get("ativo"):
        _forbidden("Permissão inválida ou desativada")

    name = perm.get("nome")
    if name not in allowed_names:
        _forbidden(f"Requer permissão {', '.join(allowed_names)}")

    return payload


def require_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency: apenas ADMIN pode acessar.
    Uso: Depends(require_admin)
    """
    return _require_permission([ADMIN_NAME], credentials)


def require_rh_or_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency: RH ou ADMIN.
    Uso: Depends(require_rh_or_admin)
    """
    return _require_permission([RH_NAME, ADMIN_NAME], credentials)


def require_gerente_or_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency: GERENTE ou ADMIN.
    Uso: Depends(require_gerente_or_admin)
    """
    return _require_permission([GERENTE_NAME, ADMIN_NAME], credentials)


def require_user_or_higher(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency: qualquer usuário autenticado (USER, GERENTE, RH, ADMIN).
    Uso: Depends(require_user_or_higher)
    """
    return _require_permission([USER_NAME, GERENTE_NAME, RH_NAME, ADMIN_NAME], credentials)
