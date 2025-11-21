from repositories import UsuariosSistemaRepository, FuncionariosRepository, PermissoesRepository

class UsuariosService:
    def __init__(self):
        self.repository = UsuariosSistemaRepository()
        self.funcionarios_repo = FuncionariosRepository()
        self.permissoes_repo =  PermissoesRepository()

    def create_usuario(self, username, password, id_permissao, id_funcionario = None):

        if self.repository.get_by_username(username):
            raise ValueError("Username já existente")
        
        #Configurare regras de SEnhas aqui

        permissao = self.permissoes_repo.get_by_id(id_permissao= id_permissao)
        if not permissao:
            raise ValueError("Permissão não encontrada.")
        if not permissao["ativo"]:
            raise ValueError("Permissão está desativada e não pode ser atribuída.")

        if id_funcionario:
            funcionario = self.funcionarios_repo.get_by_id(id_funcionario = id_funcionario)
            if not funcionario:
                raise ValueError("Funcionario não encontrado")


        return self.repository.create(username = username, password = password, id_permissao = id_permissao, id_funcionario = id_funcionario)
    

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, usuario_id):
        return self.repository.get_by_id(usuario_id)

    def update(self, usuario_id, username = None, password = None, id_permissao = None, id_funcionario = None):

        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        if username : 
            existing_user = self.repository.get_by_username(username)
            if existing_user and existing_user['id'] != usuario_id:
                raise ValueError("Username já existente")
            
        #Regras de Senha

        if id_permissao is not None:
            permissao = self.permissoes_repo.get_by_id(id_permissao=id_permissao)
            if not permissao:
                raise ValueError("Permissão não encontrada.")
            if not permissao["ativo"]:
                raise ValueError("Permissão está desativada e não pode ser atribuída.")
            
        if id_funcionario:
            funcionario = self.funcionarios_repo.get_by_id(id_funcionario = id_funcionario)
            if not funcionario:
                raise ValueError("Funcionario não encontrado")
            
        return self.repository.update(usuario_id, username= username, password = password, id_permissao = id_permissao, id_funcionario= id_funcionario)

    def delete(self, usuario_id):
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        return self.repository.delete(usuario_id)