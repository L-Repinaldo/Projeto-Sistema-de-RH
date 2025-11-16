from repositories import FuncionariosRepository as repository, SetoresRepository as setores_repo

class FuncionariosService:
    
    def __init__(self, repository = repository(), setores_repo = setores_repo()):
        self.repository = repository
        self.setores_repo = setores_repo

    
    def create(self, nome, sobrenome, cpf, email, id_setor, cargo, faixa_salarial, data_nascimento, data_admissao):

        if {self.repository.get_by_nome_completo(nome = nome, sobrenome = sobrenome) or self.repository.get_by_cpf(cpf = cpf) 
        or self.repository.get_by_email(email = email) }:
            raise ValueError("Funcionário já cadastrado.")
        

        if not self.setores_repo.get_by_id(id_setor= id_setor):
            raise ValueError("Setor não encontrado")
        
        #CADASTRAR CARGO(ROLES)

        return self.repository.create(nome = nome, sobrenome = sobrenome, cpf = cpf, email= email, id_setor = id_setor, cargo = cargo,
                                      faixa_salarial= faixa_salarial, data_nascimento= data_nascimento, data_admissao= data_admissao )