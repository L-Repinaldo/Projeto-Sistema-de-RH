from repositories import (FuncionariosRepository, SetoresRepository, BeneficioFuncionarioRepository,
                           UsuariosSistemaRepository, AvaliacoesRepository, CargosRepository)

class FuncionariosService:
    
    def __init__(self):
        self.repository = FuncionariosRepository()
        self.setores_repo = SetoresRepository()
        self.beneficio_funcionario_repo = BeneficioFuncionarioRepository()
        self.usuario_sistema_repo = UsuariosSistemaRepository()
        self.avaliacoes_repo = AvaliacoesRepository()
        self.cargos_repo = CargosRepository()

    
    def create(self, nome, sobrenome, cpf, email, id_setor, id_cargo, faixa_salarial, data_nascimento, data_admissao):

        if self.repository.get_by_nome_completo(nome = nome, sobrenome = sobrenome):
            raise ValueError("Já existe funcionário com esse nome completo.")

        if self.repository.get_by_cpf(cpf = cpf):
            raise ValueError("CPF já cadastrado.")
        
        if self.repository.get_by_email(email = email):
            raise ValueError("Email já cadastrado")
        

        if not self.setores_repo.get_by_id(id_setor= id_setor):
            raise ValueError("Setor não encontrado")
        
        cargo = self.cargos_repo.get_by_id(id_cargo= id_cargo)
        if not cargo:
            raise ValueError("Cargo não encontrado.")
        if not cargo["ativo"]:
            raise ValueError("Cargo está desativado e não pode ser atribuído.")

        return self.repository.create(nome = nome, sobrenome = sobrenome, cpf = cpf, email= email, id_setor = id_setor, id_cargo = id_cargo,
                                      faixa_salarial= faixa_salarial, data_nascimento= data_nascimento, data_admissao= data_admissao )

    def get_by_nome(self, nome):

        funcionarios =  self.repository.get_by_nome(nome= nome)
        if not funcionarios:
            raise ValueError("Nenhum funcionário com esse nome encontrado.")
        
        return funcionarios
    
    def get_by_sobrenome(self, sobrenome):

        funcionarios =  self.repository.get_by_sobrenome(sobrenome= sobrenome)
        if not funcionarios:
            raise ValueError("Nenhum funcionário com esse sobrenome encontrado.")
        
        return funcionarios
    
    def get_by_setor(self, id_setor):

        if not self.setores_repo.get_by_id(id_setor= id_setor):
            raise ValueError("Setor não encontrado.")

        funcionarios =  self.repository.get_by_setor(id_setor= id_setor)

        if not funcionarios:
            raise ValueError("Nenhum funcionário encontrado nesse setor.")
        
        return funcionarios
    

    def get_by_cargo(self, id_cargo):

        cargo = self.cargos_repo.get_by_id(id_cargo= id_cargo)
        if not cargo:
            raise ValueError("Cargo não encontrado.")

        funcionarios =  self.repository.get_by_cargo(id_cargo= id_cargo)
        if not funcionarios:
            raise ValueError("Nenhum funcionário encontrado com esse cargo.")      
        return funcionarios
    
    def get_all(self):
        return self.repository.get_all()
    
    def update(self, funcionario_id, nome = None, sobrenome = None, email = None, id_setor = None, id_cargo = None, faixa_salarial = None):
        
        funcionario = self.repository.get_by_id(funcionario_id= funcionario_id)

        if not funcionario:
            raise ValueError("Funcionário não encontrado.")
        
        if id_setor is not None and not self.setores_repo.get_by_id(id_setor= id_setor):
            raise ValueError("Setor não encontrado.")
        
        if nome:
            encontrado = self.repository.get_by_nome_completo(
                nome=nome,
                sobrenome=funcionario["sobrenome"]
            )
            if encontrado and encontrado["id"] != funcionario_id:
                raise ValueError("Já existe funcionário com esse nome completo.")

        if sobrenome:
            encontrado = self.repository.get_by_nome_completo(
                nome=funcionario["nome"],
                sobrenome=sobrenome
            )
            if encontrado and encontrado["id"] != funcionario_id:
                raise ValueError("Já existe funcionário com esse nome completo.")

        
        if email:
            existente = self.repository.get_by_email(email=email)
            if existente and existente["id"] != funcionario_id:
                raise ValueError("Email já está em uso por outro funcionário.")
        
        if id_cargo is not None:
            cargo = self.cargos_repo.get_by_id(id_cargo=id_cargo)
            if not cargo:
                raise ValueError("Cargo não encontrado.")
            if not cargo["ativo"]:
                raise ValueError("Cargo está desativado e não pode ser atribuído.")

        return self.repository.update(funcionario_id = funcionario_id, nome = nome, sobrenome = sobrenome, email = email,
                                       id_setor = id_setor, id_cargo = id_cargo, faixa_salarial = faixa_salarial)
    
    def delete(self, funcionario_id):

        funcionario = self.repository.get_by_id(funcionario_id= funcionario_id)

        if not funcionario:
            raise ValueError("Funcionário não encontrado.")
        
        setor_gerenciado =  self.setores_repo.get_by_gerente(id_gerente= funcionario_id)

        if setor_gerenciado:
            self.setores_repo.update(id_setor = setor_gerenciado["id"], id_gerente = None)

        beneficios = self.beneficio_funcionario_repo.get_by_funcionario(id_funcionario = funcionario_id)
        if beneficios:
            self.beneficio_funcionario_repo.delete_by_funcionario(id_funcionario= funcionario_id)
        
        usuario_cadastro = self.usuario_sistema_repo.get_by_funcionario_id(id_funcionario= funcionario_id)
        if usuario_cadastro:
            self.usuario_sistema_repo.delete_by_funcionario_id(id_funcionario= funcionario_id)

        avaliacoes = self.avaliacoes_repo.get_by_funcionario(id_funcionario= funcionario_id)
        if avaliacoes:
            self.avaliacoes_repo.delete_by_funcionario(id_funcionario= funcionario_id)

        return self.repository.delete(funcionario_id= funcionario_id)