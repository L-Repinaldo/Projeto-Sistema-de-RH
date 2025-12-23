from repositories.beneficios_repository import BeneficiosRepository 
class BeneficiosService:
    
    def __init__(self, repository = None):
        self.repository = repository or BeneficiosRepository()

    def create(self, nome):

        if self.repository.get_by_nome(nome):
            raise ValueError("Benefício já existente.") 
        
        return self.repository.create(nome)

    def get_by_id(self, id_beneficios):

        beneficio = self.repository.get_by_id(id_beneficios)
        if not beneficio:   
            raise ValueError("Benefício não encontrado.")  
         
        return beneficio

    def get_all(self):
        return self.repository.get_all()
    
    def delete(self, id_beneficios):

        beneficio = self.repository.get_by_id(id_beneficios)
        if not beneficio:   
            raise ValueError("Benefício não encontrado.")
        return self.repository.delete(id_beneficios)