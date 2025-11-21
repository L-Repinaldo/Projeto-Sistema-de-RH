from repositories import CargosRepository, FuncionariosRepository

class CargosService:

    def __init__(self):
        self.repository = CargosRepository()
        self.funcionarios_repo = FuncionariosRepository()
    
    def create(self, nome):

        if self.repository.get_by_name(nome = nome):
            raise ValueError("Cargo já existe.")
        
        return self.repository.create(nome= nome)
    
    def get_by_id(self, id_cargo):
        cargo = self.repository.get_by_id(id_cargo= id_cargo)

        if not cargo:
            raise ValueError("Cargo não encontrado.")
        
        return cargo
    
    def get_by_name(self, nome):
        cargo = self.repository.get_by_name(nome = nome)

        if not cargo:
            raise ValueError("Cargo não encontrado.")
        
        return cargo
    
    def update(self, id_cargo, nome):

        cargo = self.repository.get_by_id(id_cargo= id_cargo)

        if not cargo:
            raise ValueError("Cargo não encontrado.")
        
        existing_cargo = self.repository.get_by_name(nome = nome)
        if existing_cargo and existing_cargo["id"] != id_cargo:
            raise ValueError("Outro cargo com esse nome já existe.")
        
        self.repository.update(id_cargo= id_cargo, nome= nome)
        return True
    
    def desactivate(self, id_cargo):

        cargo = self.repository.get_by_id(id_cargo= id_cargo)
        if not cargo:
            raise ValueError("Cargo não encontrado.")
        if cargo['ativo'] == False:
            raise ValueError("Cargo já desativado")
        
        funcionarios_ativos = self.funcionarios_repo.get_by_cargo(id_cargo= id_cargo)
        if funcionarios_ativos:
            raise  ValueError("Não é possível desativar cargos com funcionários ativos.")
        
        self.repository.desactivate(id_cargo= id_cargo)
        return True
    
    def activate(self, id_cargo):

        cargo = self.repository.get_by_id(id_cargo = id_cargo)
        if not cargo:
            raise ValueError("Cargo não encontrado.")
        
        if cargo['ativo'] == True:
            raise ValueError("Cargo já ativado")
                
        return self.repository.activate(id_cargo= id_cargo)
