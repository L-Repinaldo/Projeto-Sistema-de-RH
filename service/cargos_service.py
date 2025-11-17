from repositories import CargosRepository

class CargosService:

    def __init__(self):
        self.repository = CargosRepository()
    
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
        
        self.repository.desactivate(id_cargo= id_cargo)
        return True
