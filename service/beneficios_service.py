from repositories.beneficios_repository import BeneficiosRepository 
class BeneficiosService:
    
    def __init__(self, repository = None):
        self.repository = repository or BeneficiosRepository()

    def create_beneficio(self, nome):
        return self.repository.create(nome)

    def get_beneficio_by_id(self, id_beneficios):
        return self.repository.get_by_id(id_beneficios)

    def get_all_beneficios(self):
        return self.repository.get_all()
    
    def delete_beneficio(self, id_beneficios):
        return self.repository.delete(id_beneficios)