from repositories import LogsAcessoRepository, UsuariosSistemaRepository
import datetime

class LogsAcessoService:
    
    def __init__(self):
        self.repository = LogsAcessoRepository()
        self.usuarios_repo = UsuariosSistemaRepository()

    def create(self, id_usuario, operacao, consulta, result_count, time_stamp=None ):

        time_stamp = time_stamp or datetime.datetime.now()

        if not self.usuarios_repo.get_by_id(id_usuarios_sistema= id_usuario):
            raise ValueError("Usuário não encontrado.")
        
        if not operacao or not isinstance(operacao, str):
            raise ValueError("Operação inválida.")

        if not consulta or not isinstance(consulta, str):
            raise ValueError("Consulta inválida.")

        if not isinstance(result_count, int) or result_count < 0:
            raise ValueError("result_count deve ser um inteiro maior ou igual a 0.")
        
        return self.repository.create( id_usuario= id_usuario, operacao= operacao, consulta= consulta,
                                       result_count= result_count, time_stamp= time_stamp )
    
    def get_all(self):

        return self.repository.get_all()

    def get_by_usuario(self, id_usuario):

        if not self.usuarios_repo.get_by_id(id_usuarios_sistema= id_usuario):
            raise ValueError("Usuário não encontrado.")

        return self.repository.get_by_usuario(id_usuario= id_usuario)


    def get_by_time_range(self, start_time, end_time):

        if start_time >= end_time:
            raise ValueError("Intervalo de tempo inválido.")

        return self.repository.get_by_time_range(start_time= start_time, end_time= end_time)