from repositories import UsuariosSistemaRepository, FuncionariosRepository

class UsuariosService:
    def __init__(self):
        self.repository = UsuariosSistemaRepository()
        self.funcionarios_repo = FuncionariosRepository()

    def create_usuario(self, username, password, role, id_funcionario = None):

        if self.repository.get_by_username(username):
            raise ValueError("Username já existente")
        
        #Configurar Role e regras de SEnhas aqui

        if id_funcionario:
            funcionario = self.funcionarios_repo.get_by_id(id_funcionario = id_funcionario)
            if not funcionario:
                raise ValueError("Funcionario não encontrado")


        return self.repository.create(username = username, password = password, role = role, id_funcionario = id_funcionario)
    

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, usuario_id):
        return self.repository.get_by_id(usuario_id)

    def update(self, usuario_id, username = None, password = None, role = None, id_funcionario = None):

        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        if username : 
            existing_user = self.repository.get_by_username(username)
            if existing_user and existing_user['id'] != usuario_id:
                raise ValueError("Username já existente")
            
        #Regras de Senha
        #Regras de roles

        if id_funcionario:
            funcionario = self.funcionarios_repo.get_by_id(id_funcionario = id_funcionario)
            if not funcionario:
                raise ValueError("Funcionario não encontrado")
            
        return self.repository.update(usuario_id, username= username, password = password, role = role, id_funcionario= id_funcionario)

    def delete(self, usuario_id):
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        return self.repository.delete(usuario_id)