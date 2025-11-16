from repositories import SetoresRepository as repository, FuncionariosRepository as funcionario_repo

class SetoresService:

    def __init__(self, repository = repository(), funcionario_repo = funcionario_repo() ):
        self.repository = repository
        self.funcionario_repo = funcionario_repo

    
    def create(self, nome, id_gerente = None):

        if self.repository.get_by_name(nome = nome):
            raise ValueError("Já existe setor com esse nome.")
        
        if id_gerente is not None:

            if not self.funcionario_repo.get_by_id(funcionario_id = id_gerente):
                raise ValueError("Gerente informado não existe")
            
            if self.repository.get_by_gerente(id_gerente= id_gerente):
                raise ValueError("Este gerente já gerencia outro setor.")
            
        return self.repository.create(nome = nome, id_gerente = id_gerente)
    
    def get_by_nome(self, nome):
        setor = self.repository.get_by_nome(nome = nome)

        if not setor:
            raise ValueError("Setor não encontrado")
        
        return setor

    def get_all(self):
        return self.repository.get_all()

    
    def update(self, id_setor, nome = None, id_gerente = None):

        setor = self.repository.get_by_id(id_setor= id_setor)
        
        if not setor:
            raise ValueError("Setor não encontrado")
        
        if nome and self.repository.get_by_name(nome= nome):
            raise ValueError("Já existe outro setor com esse nome.")
        
        if id_gerente is not None:

            if not self.funcionario_repo.get_by_id(funcionario_id= id_gerente):
                raise ValueError("Gerente informado não existe")
            
            outro_setor = self.repository.get_by_gerente(id_gerente= id_gerente)
            if outro_setor and outro_setor["id"] != id_setor:
                raise ValueError("Este gerente já gerencia outro setor.")
        

        return repository.update(id_setor, nome = nome , id_gerente = id_gerente)
            
    def delete(self, id_setor):

        setor = self.repository.get_by_id(id_setor = id_setor)

        if not setor:
            raise ValueError("Setor não encontrado.")
        
        funcionarios_no_setor = self.funcionario_repo.get_by_setor(id_setor = id_setor)
        if funcionarios_no_setor:
            raise ValueError("Não é possível excluir um setor com funcionários vinculados")
        
        return self.repository.delete(id_setor = id_setor)