from repositories import PermissoesRepository, UsuariosSistemaRepository

class PermissoesService:

    def __init__(self):
        self.repository = PermissoesRepository()
        self.usuarios_repo = UsuariosSistemaRepository()

    
    def create(self, nome):

        permissao = self.repository.get_by_nome(nome = nome)

        if permissao:
            raise ValueError("Permissão já existente")

        return self.repository.create(nome = nome)
    
    def get_all(self):
        return self.repository.get_all()

    
    def get_by_nome(self, nome):

        permissao = self.repository.get_by_nome(nome = nome)

        if not permissao:
            raise ValueError("Permissão não encontrada")
        
        return permissao
    
    def update(self, id_permissao, nome):

        permissao = self.repository.get_by_id(id_permissao= id_permissao)

        if not permissao:
            raise ValueError("Permissão não encontrada")
        
        existing_permissao = self.repository.get_by_nome(nome = nome)
        if existing_permissao and existing_permissao['id'] != id_permissao:
            raise ValueError("Outra permissão com esse nome já existe.")
        
        return self.repository.update(id_permissao= id_permissao, nome = nome)
    
    def desactivate(self, id_permissao):

        permissao = self.repository.get_by_id(id_permissao = id_permissao)

        if not permissao:
            raise ValueError("Permissão não existente")
        
        if permissao['ativo'] == False:
            raise ValueError("Permissão já desativada")

        usuarios_com_permissao = self.usuarios_repo.get_by_permissao(id_permissao = id_permissao)
        if usuarios_com_permissao:
            raise ValueError("Não é possível desativar a permissão, existem usuários associados a ela.")
        
        return self.repository.desactivate(id_permissao= id_permissao)
    
    def activate(self, id_permissao):

        permissao = self.repository.get_by_id(id_permissao = id_permissao)

        if not permissao:
            raise ValueError("Permissão não existente")
        
        if permissao['ativo'] == True:
            raise ValueError("Permissão já ativada")
        
        return self.repository.activate(id_permissao= id_permissao)