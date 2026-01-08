from fastapi import FastAPI
from controllers import (
    usuarios_controller,
    avaliacoes_controller,
    beneficios_controller,
    beneficios_funcionarios_controller,
    cargos_controller,
    funcionario_controller,
    logs_acesso_controller,
    permissoes_controller,
    setores_controller,
    populacao_rapida_controller
)

from utils.audit_logger import configure_logger
from service.logs_acesso_service import LogsAcessoService


app = FastAPI(title="Sistema de RH", description="API para gerenciamento de recursos humanos")

logs_service = LogsAcessoService()
configure_logger(logs_service.create)


# Include routers
app.include_router(usuarios_controller.router)
app.include_router(avaliacoes_controller.router)
app.include_router(beneficios_controller.router)
app.include_router(beneficios_funcionarios_controller.router)
app.include_router(cargos_controller.router)
app.include_router(funcionario_controller.router)
app.include_router(logs_acesso_controller.router)
app.include_router(permissoes_controller.router)
app.include_router(setores_controller.router)
app.include_router(populacao_rapida_controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086)
