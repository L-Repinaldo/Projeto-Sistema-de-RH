from faker import Faker
import random
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

    # ======================================================
    # Método principal
    # ======================================================

    def populate_system(self, qtd_funcionarios: int, current_user: dict):


        setores = self._get_setores()
        cargos = self._get_cargos()
        beneficios_por_cargo = self._map_beneficios_por_cargo()

        funcionarios_ids = self._create_funcionarios(
            qtd_funcionarios=qtd_funcionarios,
            setores=setores,
            cargos=cargos
        )

        self._vincular_beneficios(funcionarios_ids, beneficios_por_cargo)
        self._criar_avaliacoes(funcionarios_ids)



    # ======================================================
    # Criação de funcionários
    # ======================================================

    def _create_funcionarios(self, qtd_funcionarios: int, setores: list, cargos: list):

        funcionarios_ids = []

        for _ in range(qtd_funcionarios):

            nome = self.fake.first_name()
            sobrenome = self.fake.last_name()
            cpf = self.fake.cpf()

            id_setor = random.choice(setores)
            id_cargo = random.choice(cargos)

            cargo = self.cargo_repo.get_by_id(id_cargo=id_cargo)
            cargo_nome = cargo["nome"]

            email = f"{nome.lower()}.{sobrenome.lower()}@empresa.com"

            salario = self._gerar_salario(cargo_nome)

            data_nascimento = self._random_date(1960, 2016)
            data_admissao = self._random_date(2015, 2025)

            funcionario_id = self.func_service.create(
                nome=nome,
                sobrenome=sobrenome,
                cpf=cpf,
                email=email,
                id_setor=id_setor,
                id_cargo=id_cargo,
                salario=salario,
                data_nascimento=data_nascimento,
                data_admissao=data_admissao
            )

            funcionarios_ids.append(funcionario_id)

        return funcionarios_ids

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
        return [c["id"] for c in cargos if c["id"] != 3]

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

    def _gerar_salario(self, cargo_nome: str):

        ranges = {
            "Administrador do Sistema": (4000, 10000),
            "Analista de RH": (3000, 11000),
            "Gerente": (4000, 15000),
            "Funcionário": (1200, 3000),
        }

        minimo, maximo = ranges.get(cargo_nome, (3000, 5000))
        return random.randint(minimo, maximo)

    def _random_date(self, start_year: int, end_year: int):

        start = date(start_year, 1, 1)
        end = date(end_year, 12, 31)
        delta = (end - start).days

        return start + timedelta(days=random.randint(0, delta))
