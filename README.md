# Projeto-Sistema-de-RH
🧭 Resumo -> Sistema de Recursos Humanos com Controle de Acesso e Auditoria

Este projeto consiste em um Sistema de Recursos Humanos (RH) desenvolvido para gerenciar informações organizacionais e operacionais de forma segura, auditável e alinhada às boas práticas de privacidade.

A aplicação foi projetada como uma API REST profissional, com controle rigoroso de permissões, separação clara de responsabilidades e mecanismos de rastreabilidade de operações sensíveis.

🎯 Objetivo Geral

O sistema tem como objetivo:

  - Gerenciar dados de funcionários, cargos, setores, avaliações e benefícios.
  
  - Implementar controle de acesso baseado em papéis (RBAC).
  
  - Garantir segregação de privilégios entre diferentes tipos de usuários.
  
  - Registrar operações relevantes por meio de logs de acesso auditáveis.
  
  - Atender princípios fundamentais da LGPD, como minimização, necessidade e rastreabilidade.

⚙️ Tecnologias Utilizadas

  - FastAPI — backend e definição da API REST
  
  - PostgreSQL — banco de dados relacional
  
  - SQLAlchemy / Repositórios customizados — acesso a dados
  
  - Pydantic — validação e serialização de schemas
  
  - JWT / Dependências de autenticação — segurança e autorização
  
  - Arquitetura em camadas — controllers, services, repositories e utils

🏗️ Estrutura do Banco de Dados (visão geral)
  1. Funcionários (funcionarios)
  
  Armazena dados pessoais e profissionais dos colaboradores, como setor, cargo, status e informações administrativas.
  
  2. Setores (setores)
  
  Define as áreas da organização, permitindo associação com funcionários e responsáveis.
  
  3. Cargos (cargos)
  
  Gerencia cargos existentes na empresa e suas relações organizacionais.
  
  4. Avaliações (avaliacoes)
  
  Registra avaliações de desempenho, notas e observações periódicas.
  
  5. Benefícios (beneficios)
  
  Mantém o catálogo de benefícios disponíveis na organização.
  
  6. Benefícios por Funcionário (beneficios_funcionarios)
  
  Relaciona benefícios específicos a funcionários, controlando vínculo e status.
  
  7. Usuários do Sistema (usuarios_sistema)
  
  Controla autenticação, credenciais e o papel de cada usuário no sistema.
  
  8. Logs de Acesso (logs_acesso)
  
   Registra operações relevantes realizadas na API, garantindo:
  
   - rastreabilidade,
  
   - auditoria,
  
   -   apoio a investigações e conformidade legal.
     
 9. Permissões (permissoes)
     
   Gerencia permissões existentes no sistema da empresa.
 

🔐 Controle de Acesso (RBAC)

O sistema implementa controle de acesso baseado em papéis, garantindo que cada usuário execute apenas operações compatíveis com sua função.

Papéis suportados incluem, por exemplo:

- Usuário comum

- Analista

- Gerência

- RH

- Administrador

O controle é aplicado via:

- dependências do FastAPI (Depends)

- validação centralizada de permissões

- separação clara entre endpoints públicos e restritos


🧾 Auditoria e Logs de Acesso

O sistema registra automaticamente operações relevantes, como:

- consultas a listas

- acessos administrativos

- operações de criação, atualização e exclusão

Os logs armazenam informações como:

- usuário responsável

- tipo de operação

- contexto da ação

- timestamp

- volume de resultados (quando aplicável)

Consultas altamente sensíveis são tratadas de forma controlada, evitando exposição indevida de dados nos registros.

🔒 Privacidade e Conformidade

O projeto foi desenvolvido considerando princípios fundamentais de proteção de dados, como:

- necessidade: acesso apenas ao que é estritamente necessário

- finalidade: dados usados apenas para fins administrativos

- rastreabilidade: todas as ações relevantes são auditáveis

- segregação de acesso: dados sensíveis protegidos por papel

Esses cuidados tornam o sistema compatível com boas práticas exigidas por legislações como a LGPD.

📁 Estrutura Geral do Projeto

    backend/
    ├── controllers/        # Endpoints da API
    ├── service/            # Regras de negócio
    ├── repository/         # Acesso ao banco de dados
    ├── schemas/            # Schemas Pydantic
    ├── utils/              # Autenticação, autorização e auditoria
    ├── app.py              # Inicialização da aplicação

    frontend/
    ├── paginas/            # Front para o acesso aos controllers da API
    ├── auth.py             # Tela de login
    ├── layout.py           # Implementação sidebar
    ├── utils.py            # Tratamento de erro caso autorização não permitida
    ├── app.py 

📌 Considerações Finais

Este sistema foi desenvolvido com foco em robustez, clareza arquitetural e segurança, representando uma aplicação de RH realista, auditável e extensível.

Ele demonstra domínio de:

- arquitetura backend,

- controle de acesso,

- boas práticas de privacidade,

- e desenvolvimento de APIs profissionais.
