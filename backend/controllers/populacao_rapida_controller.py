from fastapi import APIRouter, Depends, HTTPException
from utils import require_admin, log_access
from service import PopulacaoRapidaService

router = APIRouter( prefix="/admin/populacao", tags=["Administração"])

service = PopulacaoRapidaService()


@router.post("/sistema")
def populate_system(qtd_funcionarios: int = 100, current_user: dict = Depends(require_admin)
):
    try:

        log_access(
            user_id=current_user["id"],
            operacao="SEED_SYSTEM_START",
            consulta="População rápida do sistema"
        )

        service.populate_system(
            qtd_funcionarios=qtd_funcionarios,
            current_user=current_user
        )

        log_access(
            user_id=current_user["id"],
            operacao="SEED_SYSTEM_END",
            consulta="População concluída",
            result_count=qtd_funcionarios
        )
        
        return {
            "message": "Sistema populado com sucesso",
            "funcionarios_criados": qtd_funcionarios
        }

    except Exception as e:
        log_access(
            user_id=current_user["id"],
            operacao="SEED_SYSTEM_ERROR",
            consulta=str(e)
        )
        raise HTTPException(status_code=400, detail=str(e))
