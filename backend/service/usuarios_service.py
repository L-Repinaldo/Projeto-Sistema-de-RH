from repositories import UsuariosSistemaRepository, FuncionariosRepository, PermissoesRepository
from utils import PasswordUtil
from utils.jwt_util import create_access_token

class UsuariosService:
    def __init__(self):
        self.repository = UsuariosSistemaRepository()
        self.funcionarios_repo = FuncionariosRepository()
        self.permissoes_repo =  PermissoesRepository()

    def create(self, username, password, id_permissao, id_funcionario = None):

        if self.repository.get_by_username(username):
            raise ValueError("Username já existente")
        
        hashed = PasswordUtil.hash_password(raw_password= password)

        permissao = self.permissoes_repo.get_by_id(id_permissao= id_permissao)
        if not permissao:
            raise ValueError("Permissão não encontrada.")
        if not permissao["ativo"]:
            raise ValueError("Permissão está desativada e não pode ser atribuída.")

        if id_funcionario:
            funcionario = self.funcionarios_repo.get_by_id( funcionario_id = id_funcionario)
            if not funcionario:
                raise ValueError("Funcionario não encontrado")


        return self.repository.create(username = username, password = hashed, id_permissao = id_permissao, id_funcionario = id_funcionario)
    

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
        
        hashed = None
        if password:
            hashed = PasswordUtil.hash_password(raw_password= password)

        if id_permissao is not None:
            permissao = self.permissoes_repo.get_by_id(id_permissao=id_permissao)
            if not permissao:
                raise ValueError("Permissão não encontrada.")
            if not permissao["ativo"]:
                raise ValueError("Permissão está desativada e não pode ser atribuída.")
            
        if id_funcionario:
            funcionario = self.funcionarios_repo.get_by_id(funcionario_id = id_funcionario)
            if not funcionario:
                raise ValueError("Funcionario não encontrado")
            
        return self.repository.update(usuario_id, username= username, password = hashed, id_permissao = id_permissao, id_funcionario= id_funcionario)

    def delete(self, usuario_id):
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario não encontrado")
        
        return self.repository.delete(usuario_id)
    

    def login(self, username: str, password: str):

        usuario = self.repository.get_by_username(username = username)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        hashed = usuario["password"]
        if not PasswordUtil.verify_password(raw_password= password, hashed_password= hashed):
            raise ValueError("Credenciais inválidas")

        token_data = {"sub": str(usuario["id"]), "username": usuario["username"], "id_permissao" : usuario["id_permissao"]}
        access_token = create_access_token(data=token_data)

        permissao = self.permissoes_repo.get_by_id(id_permissao= usuario["id_permissao"])
        return {"usuario": usuario["username"], "permissao" : permissao["nome"], "access_token": access_token, "token_type": "bearer"}
