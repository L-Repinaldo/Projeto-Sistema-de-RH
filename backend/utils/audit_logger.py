import datetime
from typing import Callable

# Função que será injetada em runtime
_log_writer: Callable | None = None


def configure_logger(log_writer: Callable):

    global _log_writer
    _log_writer = log_writer


def log_access(
    *,
    id_usuario: int,
    operacao: str,
    consulta: str,
    result_count: int
):
    if not _log_writer:
        return  # fail silent: não quebra o sistema

    _log_writer(
        id_usuario=id_usuario,
        operacao=operacao,
        consulta=consulta,
        result_count=result_count,
        time_stamp=datetime.datetime.now()
    )
