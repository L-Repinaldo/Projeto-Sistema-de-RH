from repositories import BeneficioFuncionarioRepository, FuncionariosRepository, BeneficiosRepository

class BeneficiosFuncionariosService:
    def __init__(self):
        self.repository = BeneficioFuncionarioRepository()
        self.funcionarios_repo = FuncionariosRepository()
        self.beneficios_repo = BeneficiosRepository()

    def create(self, funcionario_id, beneficio_id, ativo = True):
        funcionario = self.funcionarios_repo.get_by_id(funcionario_id)
        beneficio = self.beneficios_repo.get_by_id(beneficio_id)

        if not funcionario:
            raise ValueError("Funcionário não encontrado.")
        if not beneficio:
            raise ValueError("Benefício não encontrado.")
        
        existente = self.repository.get_by_funcionario_e_beneficio(id_funcionario = funcionario_id, id_beneficio = beneficio_id)
        if existente:
            raise ValueError("O funcionário já possui este benefício atribuído.")

        return self.repository.create(id_funcionario= funcionario_id, id_beneficio= beneficio_id, ativo = ativo)

    def get_all(self):
        return self.repository.get_all()
    
    def get_by_funcionario(self, funcionario_id):

        funcionario = self.funcionarios_repo.get_by_id(funcionario_id)
        if not funcionario:
            raise ValueError ("Funcionário não encontrado.")

        return funcionario
    
    def get_by_beneficio(self, beneficio_id):

        beneficio = self.beneficios_repo.get_by_id(beneficio_id)
        if not beneficio:
            raise ValueError ("Benefício não encontrado.")

        return beneficio

    def update(self, id_beneficio_funcionario, ativo):

        beneficio_funcionario = self.repository.get_by_id(id_beneficio_funcionario)
        if not beneficio_funcionario:
            raise ValueError("Benefício do funcionário não encontrado.")
        
        return self.repository.update(id_beneficio_funcionario = id_beneficio_funcionario, ativo = ativo)
    
    def delete(self, id_beneficio_funcionario):

        beneficio_funcionario = self.repository.get_by_id(id_beneficio_funcionario)
        if not beneficio_funcionario:
            raise ValueError("Benefício do funcionário não encontrado.")
        
        return self.repository.delete(id_beneficio_funcionario)