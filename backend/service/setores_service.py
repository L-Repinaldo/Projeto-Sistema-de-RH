from repositories import SetoresRepository , FuncionariosRepository

class SetoresService:

    def __init__(self, repository = None , funcionario_repo = None ):
        self.repository = repository or SetoresRepository()
        self.funcionario_repo = funcionario_repo or FuncionariosRepository()

    
    def create(self, nome, id_gerente = None):

        if self.repository.get_by_name(nome = nome):
            raise ValueError("Já existe setor com esse nome.")
        
        if id_gerente is not None:

            if not self.funcionario_repo.get_by_id(funcionario_id = id_gerente):
                raise ValueError("Gerente informado não existe")
            
            if self.repository.get_by_gerente(id_gerente= id_gerente):
                raise ValueError("Este gerente já gerencia outro setor.")
            
        return self.repository.create(nome = nome, id_gerente = id_gerente)
    
    def get_by_name(self, nome):
        setor = self.repository.get_by_name(nome = nome)

        if not setor:
            raise ValueError("Setor não encontrado")
        
        return setor

    def get_all(self):
        return self.repository.get_all()

    
    def update(self, id_setor, nome = None, id_gerente = None):

        setor = self.repository.get_by_id(id_setor= id_setor)
        
        if not setor:
            raise ValueError("Setor não encontrado")
        
        if nome is not None:
            setor_com_nome = self.repository.get_by_name(nome=nome)
            if setor_com_nome and setor_com_nome["id"] != id_setor:
                raise ValueError("Já existe outro setor com esse nome.")
            else:
                setor["nome"] = nome
        
        if id_gerente is not None:

            if not self.funcionario_repo.get_by_id(funcionario_id= id_gerente):
                raise ValueError("Gerente informado não existe")
            
            outro_setor = self.repository.get_by_gerente(id_gerente= id_gerente)
            if outro_setor and outro_setor["id"] != id_setor:
                raise ValueError("Este gerente já gerencia outro setor.")
        

        return self.repository.update(id_setor = id_setor, nome = nome , id_gerente = id_gerente)
            
    def delete(self, id_setor):

        setor = self.repository.get_by_id(id_setor = id_setor)

        if not setor:
            raise ValueError("Setor não encontrado.")
        
        funcionarios_no_setor = self.funcionario_repo.get_by_setor(id_setor = id_setor)
        if funcionarios_no_setor:
            raise ValueError("Não é possível excluir um setor com funcionários vinculados")
        
        return self.repository.delete(id_setor = id_setor)