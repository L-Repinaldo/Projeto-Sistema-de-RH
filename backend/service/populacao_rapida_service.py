from faker import Faker
import random
import re
from datetime import date, timedelta

from repositories import (
    FuncionariosRepository,
    SetoresRepository,
    CargosRepository,
    BeneficiosRepository,
    BeneficioFuncionarioRepository,
    AvaliacoesRepository,
)

from service import (
    FuncionariosService,
    BeneficiosFuncionariosService,
    AvaliacoesService
)


class PopulacaoRapidaService:

    def __init__(self):
        self.fake = Faker("pt_BR")

        self.func_repo = FuncionariosRepository()
        self.setor_repo = SetoresRepository()
        self.cargo_repo = CargosRepository()
        self.benef_repo = BeneficiosRepository()
        self.benef_func_repo = BeneficioFuncionarioRepository()
        self.avaliacoes_repo = AvaliacoesRepository()

        self.func_service = FuncionariosService()
        self.benef_func_service = BeneficiosFuncionariosService()
        self.aval_service = AvaliacoesService()

        self.emails_usados = self._carregar_emails_existentes()

    # ======================================================
    # Método principal
    # ======================================================

    def populate_system(self, qtd_funcionarios: int):

        setores = self._get_setores()
        cargos = self._get_cargos()
        beneficios_por_cargo = self._map_beneficios_por_cargo()

        funcionarios_ids = self._create_funcionarios(
            qtd_funcionarios=qtd_funcionarios,
            setores=setores,
            cargos=cargos
        )
        print("criou")

        if not funcionarios_ids:
            raise ValueError("Nenhum funcionário foi criado.")

        self._vincular_beneficios(funcionarios_ids, beneficios_por_cargo)
        print("vinculou")
        self._criar_avaliacoes(funcionarios_ids)
        print("avaliou")
        self._recalcular_salarios(funcionarios_ids) 
        print("Terminou")

    # ======================================================
    # Criação de funcionários
    # ======================================================

    def _create_funcionarios(self, qtd_funcionarios, setores: list, cargos: list):

        funcionarios_ids = []

        i = 0

        for _ in range(int(qtd_funcionarios)):
            try:
                nome = self.fake.first_name()
                sobrenome = self.fake.last_name()

                cpf = re.sub(r"\D", "", self.fake.cpf())

                id_setor = random.choice(setores)
                id_cargo = random.choice(cargos)

                cargo = self.cargo_repo.get_by_id(id_cargo=id_cargo)
                cargo_nome = cargo["nome"]

                email = self._gerar_email_unico(nome, sobrenome)

                salario_base = self._salario_base_por_cargo(cargo_nome)

                data_nascimento = self._random_date(1960, 2006)
                data_admissao = self._random_date(2015, 2025)

                funcionario_id = self.func_service.create(
                    nome=nome,
                    sobrenome=sobrenome,
                    cpf=cpf,
                    email=email,
                    id_setor=id_setor,
                    id_cargo=id_cargo,
                    salario=salario_base,
                    data_nascimento=data_nascimento,
                    data_admissao=data_admissao
                )

                funcionarios_ids.append(funcionario_id)
                i+=1
                print(i)

            except Exception as e:
                print(f"[SEED] Erro ao criar funcionário, pulando: {e}")
                continue

        return funcionarios_ids
    

    # ======================================================
    # Salário base por cargo 
    # ======================================================

    def _salario_base_por_cargo(self, cargo_nome: str):

        bases = {
            "Administrador do Sistema": (5000, 8000),
            "Analista de RH": (4000, 7000),
            "Gerente": (8000, 12000),
            "Funcionário": (1500, 2500),
        }

        minimo, maximo = bases.get(cargo_nome, (3000, 5000))
        return random.randint(minimo, maximo)
    
    # ======================================================
    # RECÁLCULO REAL DE SALÁRIO
    # ======================================================

    def _recalcular_salarios(self, funcionarios_ids):

        ano_atual = date.today().year

        for func_id in funcionarios_ids:

            func = self.func_repo.get_by_id(funcionario_id=func_id)

            salario_base = float(func['salario'])

            anos_empresa = max(0, ano_atual - func["data_admissao"].year)

            avals = self.avaliacoes_repo.get_by_funcionario(func_id)
            if avals:
                media_notas = sum(a["nota"] for a in avals) / len(avals)
            else:
                media_notas = 5.0  # neutro

            bonus_tempo = 2200 * (1 - pow(2.71828, -anos_empresa / 6))
            bonus_desempenho = media_notas * 220

            salario_final = salario_base + bonus_tempo + bonus_desempenho
            salario_final = max(1200, round(salario_final, 2))

            self.func_service.update_salario(func_id, salario_final)

    # ======================================================
    # Email único
    # ======================================================

    def _carregar_emails_existentes(self):
        funcionarios = self.func_repo.get_all()
        if not funcionarios:
            return set()
        return {f["email"] for f in funcionarios if f.get("email")}

    def _gerar_email_unico(self, nome, sobrenome):
        base = f"{nome.lower()}.{sobrenome.lower()}@empresa.com"
        email = base
        contador = 1

        while email in self.emails_usados:
            email = f"{nome.lower()}.{sobrenome.lower()}{contador}@empresa.com"
            contador += 1

        self.emails_usados.add(email)
        return email
    

    # ======================================================
    # Vínculo de benefícios
    # ======================================================

    def _vincular_beneficios(self, funcionarios_ids: list, beneficios_por_cargo: dict):

        for func_id in funcionarios_ids:
            funcionario = self.func_repo.get_by_id(funcionario_id=func_id)
            id_cargo = funcionario["id_cargo"]

            cargo = self.cargo_repo.get_by_id(id_cargo=id_cargo)
            cargo_nome = cargo["nome"]

            for beneficio_id in beneficios_por_cargo.get(cargo_nome, []):
                self.benef_func_service.create(
                    funcionario_id=func_id,
                    beneficio_id=beneficio_id,
                    ativo=True
                )

    # ======================================================
    # Avaliações
    # ======================================================

    def _criar_avaliacoes(self, funcionarios_ids: list):

        for func_id in funcionarios_ids:

            func = self.func_repo.get_by_id(funcionario_id=func_id)

            min_date = func["data_admissao"].year + 1

            if min_date > 2025:
                continue
            
            qtd_avaliacoes = 2025 - min_date

            for _ in range(qtd_avaliacoes):
                self.aval_service.create(
                    id_funcionario=func_id,
                    nota=round(random.uniform(0.0, 10.0), 1),
                    data_avaliacao=self._random_date(min_date, 2025),
                )

    # ======================================================
    # Helpers
    # ======================================================

    def _get_setores(self):
        setores = self.setor_repo.get_all()
        if not setores:
            raise ValueError("Setores indisponíveis.")
        return [s["id"] for s in setores]

    def _get_cargos(self):
        cargos = self.cargo_repo.get_all()
        if not cargos:
            raise ValueError("Cargos indisponíveis.")
        return [c["id"] for c in cargos if c["id"] != 3 and c["id"] != 1]

    def _map_beneficios_por_cargo(self):

        beneficios = self.benef_repo.get_all()
        if not beneficios:
            raise ValueError("Benefícios indisponíveis.")

        ids = [b["id"] for b in beneficios]

        return {
            "Administrador do Sistema": [i for i in ids if i <= 6],
            "Analista de RH": [i for i in ids if i <= 6],
            "Gerente": ids,
            "Funcionário": [i for i in ids if i <= 3],
        }

    def _random_date(self, start_year: int, end_year: int):

        start = date(start_year, 1, 1)
        end = date(end_year, 12, 31)
        delta = (end - start).days

        return start + timedelta(days=random.randint(0, delta))
