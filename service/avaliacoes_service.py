from repositories import AvaliacoesRepository, FuncionariosRepository
import datetime

class AvaliacoesService:
    
    def __init__(self):
        self.repository = AvaliacoesRepository()
        self.funcionarios_repo = FuncionariosRepository()

    def create(self, id_funcionario, data_avaliacao, nota):

        if nota < 0 or nota > 10:
            raise ValueError("A nota deve estar entre 0 e 10.")
        
        if isinstance(data_avaliacao, datetime.datetime):
            data_avaliacao = data_avaliacao.date()
        
        if data_avaliacao > datetime.date.today():
            raise ValueError("A data da avaliação não pode ser no futuro.")
        
        if not self.funcionarios_repo.get_by_id(id_funcionario = id_funcionario):
            raise ValueError("Funcionário não encontrado.")
        
        return self.repository.create(id_funcionario= id_funcionario, data_avaliacao= data_avaliacao, nota= nota)
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_funcionario(self, id_funcionario):

        funcionario =  self.funcionarios_repo.get_by_id(id_funcionario = id_funcionario)
        if not funcionario:
            raise ValueError("Funcionário não encontrado.")
        
        avaliacoes = self.repository.get_by_funcionario(id_funcionario= id_funcionario)
        return avaliacoes
    

    def get_by_date_range(self, start_date, end_date):

        if isinstance(start_date, datetime.datetime):
            start_date = start_date.date()
            
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.date()


        if start_date > end_date:
            raise ValueError("A data de início não pode ser posterior à data de término.")
        
        avaliacoes =self.repository.get_by_date_range(start_date= start_date, end_date= end_date)

        return avaliacoes
    
    def get_by_nota_range(self, min_nota, max_nota):

        if min_nota < 0 or max_nota > 10 or min_nota > max_nota:
            raise ValueError("Intervalo de notas inválido. As notas devem estar entre 0 e 10.")
        
        return self.repository.get_by_nota_range(min_nota= min_nota, max_nota= max_nota)
            

    def delete(self, avaliacao_id):

        avaliacao = self.repository.get_by_id(avaliacao_id= avaliacao_id)
        if not avaliacao:
            raise ValueError("Avaliação não encontrada.")
        
        return self.repository.delete(avaliacao_id= avaliacao_id)

