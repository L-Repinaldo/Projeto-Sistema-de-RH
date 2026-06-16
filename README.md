# Projeto-Sistema-de-RH

## Visão Geral

Este repositório contém uma API Python que gera e gerencia dados sintéticos para um experimento de recursos humanos. A aplicação funciona como uma API REST comum, usando métodos HTTP `GET`, `POST`, `PUT` e `DELETE` para os fluxos de mensagem.

A proposta principal é produzir dados corporativos sintéticos para testes e experimentos, armazenados em um banco de dados PostgreSQL, e expostos via endpoints controlados por autenticação JWT e autorização baseada em permissões.

## Papel no Experimento

Essa API tem o papel exclusivo de gerar dados sintéticos que serão utilizados no experimento. Ela foi desenvolvida em Python, utilizando o paradigma de Programação Orientada a Objetos e bibliotecas como FastAPI, Pydantic, psycopg2, Faker, bcrypt, PyJWT e Streamlit.

A aplicação serve como sistema gerador de dados de RH e não é um pipeline de modelagem ou visualização experimental. Ela produz e disponibiliza o dataset sintético por meio de uma API, permitindo que outras camadas do experimento consumam esses dados.

---

## Arquitetura Geral

A arquitetura do projeto é separada em duas camadas principais:

- **Backend**: API FastAPI com controllers, services, repositories e utilitários.
- **Frontend**: aplicação Streamlit que consome a API e apresenta interfaces de CRUD.

### Backend

O backend segue uma arquitetura em camadas:

- `controllers/`: expõem endpoints HTTP do FastAPI.
- `service/`: implementam regras de negócio e validações.
- `repositories/`: executam SQL raw no PostgreSQL via `psycopg2`.
- `utils/`: cuidam de autenticação, autorização e auditoria.
- `config/connection.py`: abre conexão com PostgreSQL usando variáveis de ambiente.

### Frontend

O frontend é uma aplicação Streamlit que:

- exibe tela de login em `frontend/auth.py`;
- constrói navegação em `frontend/layout.py`;
- chama páginas em `frontend/paginas/*.py`;
- realiza requisições HTTP para a API em `http://localhost:8086`.

---

## Fluxo de Geração de Dados Sintéticos

A geração sintética é acionada pelo endpoint administrativo:

- `POST /admin/populacao/sistema`

Esse endpoint é implementado em `backend/controllers/populacao_rapida_controller.py` e chama `backend/service/populacao_rapida_service.py`.

O fluxo principal é:

1. Carregar setores e cargos existentes do banco.
2. Criar funcionários sintéticos usando Faker.
3. Sorteá-los para um setor e um cargo.
4. Definir salário base de acordo com o cargo.
5. Atribuir benefícios conforme o cargo.
6. Criar avaliações para cada funcionário.
7. Recalcular o salário conforme tempo de empresa e média das avaliações.

O módulo de população rápida foi desenvolvido para gerar volume considerável de dados e automatizar o processo de preenchimento do sistema.

---

## Entidades e Estrutura do Banco

O modelo de dados é orientado a um cenário de RH e pode ser entendido como um DER de relacionamento entre:

- `funcionarios`
- `setores`
- `cargos`
- `avaliacoes`
- `beneficios`
- `beneficio_funcionario`
- `usuarios_sistema`
- `permissoes`
- `logs_acesso`

### Relacionamentos principais

- `funcionarios.id_setor -> setores.id`
- `funcionarios.id_cargo -> cargos.id`
- `beneficio_funcionario.id_funcionario -> funcionarios.id`
- `beneficio_funcionario.id_beneficio -> beneficios.id`
- `avaliacoes.id_funcionario -> funcionarios.id`
- `usuarios_sistema.id_funcionario -> funcionarios.id`
- `usuarios_sistema.id_permissao -> permissoes.id`
- `logs_acesso.id_usuario -> usuarios_sistema.id`

### Regras de negócio relevantes

- cargos podem ser ativos ou desativados e só podem ser atribuídos se estiverem ativos.
- setores podem ter um gerente único associado.
- usuários do sistema carregam credenciais e papel de acesso.
- o recalculo salarial considera tempo de empresa e média das notas das avaliações.

---

## Fluxo do Backend

1. `backend/app.py` cria a instância FastAPI e inclui todos os routers.
2. Requisições chegam nos controllers em `backend/controllers/`.
3. Controllers usam dependências de autorização de `backend/utils/auth_dependecies.py`.
4. Controllers chamam services correspondentes em `backend/service/`.
5. Services executam validações de negócio e chamam repositories.
6. Repositories executam SQL no PostgreSQL via `backend/config/connection.py`.
7. Operações sensíveis são auditadas em `backend/utils/audit_logger.py`.

### Autenticação e autorização

- JWT é gerado em `backend/service/usuarios_service.py` com `backend/utils/jwt_util.py`.
- Permissões são validadas em `backend/utils/auth_dependecies.py`.
- Tipos de acesso incluem ADMIN, RH, GERENTE e USER.

---

## Fluxo do Frontend

1. `frontend/app.py` inicia o Streamlit.
2. Usuário faz login em `frontend/auth.py`.
3. Token JWT é armazenado em `st.session_state`.
4. `frontend/layout.py` exibe menu e carrega a página correta.
5. Cada página em `frontend/paginas/*.py` consome a API via `requests`.
6. Respostas 401/403 são tratadas em `frontend/utils.py`.

As páginas de frontend fornecem interfaces de CRUD para:

- Funcionários
- Avaliações
- Benefícios
- Cargos
- Setores
- Usuários do sistema
- Permissões
- Logs de acesso
- Benefícios por funcionário
- Administração / população rápida

---

## Estrutura de Diretórios

```text
.
├── backend/
│   ├── app.py
│   ├── config/
│   │   └── connection.py
│   ├── controllers/
│   ├── repositories/
│   ├── schemas/
│   ├── service/
│   └── utils/
├── frontend/
│   ├── app.py
│   ├── auth.py
│   ├── layout.py
│   ├── utils.py
│   └── paginas/
├── requirements.txt
└── README.md
```

---

## Instalação

1. Crie um ambiente virtual Python.
2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Configure variáveis de ambiente em um arquivo `.env` ou no ambiente:

```env
DB_USER=<usuario>
DB_PASS=<senha>
DB_HOST=<host>
DB_PORT=<porta>
SECRET_KEY=<chave-secreta>
```

4. Inicie o backend:

```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8086
```

5. Inicie o frontend:

```bash
streamlit run frontend/app.py
```

---

## Observações Técnicas

- O backend usa `psycopg2` e SQL bruto, não ORM.
- O frontend consome a API por HTTP em `http://localhost:8086`.
- O módulo de geração de dados sintéticos é `backend/service/populacao_rapida_service.py`.
- A aplicação foi desenvolvida com foco acadêmico e para uso em experimentos de dados sintéticos.
- O token JWT deve ser protegido em produção; o valor padrão de `SECRET_KEY` no código é apenas um fallback de desenvolvimento.

---

## Considerações de Privacidade

- Os dados gerados são sintéticos e não representam indivíduos reais.
- A API permite rastreabilidade via logs de acesso.
- O sistema implementa controle de acesso baseado em permissões e papéis.
- O foco está na criação e gestão de dados sintéticos para experimentos, não na aplicação de mecanismos de privacidade diferencial.

---

## Licença

Uso acadêmico e educacional.
