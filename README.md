# Projeto-Sistema-de-RH
🧭 Resumo do Projeto A — Sistema de RH com BI, Controles de Acesso e Privacidade

Este projeto é um Sistema de Recursos Humanos focado em três pilares principais:
gestão de dados sensíveis, visualização inteligente de informações e controle rigoroso de acesso.
Ele serve como uma aplicação profissional completa, adequada para portfólio, e como base estruturada para experimentos posteriores com privacidade (Projeto B (Machine Learning) ).

🎯 Objetivo Geral

Construir um sistema de RH capaz de:

Gerenciar informações de funcionários, setores, avaliações e benefícios.

Oferecer dashboards interativos e exportação de relatórios.

Implementar controle de acesso baseado em papéis, com views específicas para cada tipo de usuário.

Aplicar Privacidade Diferencial em consultas estatísticas sensíveis (como médias, contagens e distribuições).

Atender aos princípios da LGPD no tratamento de dados pessoais.

🏗️ Estrutura do Banco de Dados (visão geral)
1. Funcionários (funcionarios)

Contém dados pessoais e profissionais essenciais: setor, cargo, faixa salarial, idade e data de admissão.

2. Setores (setores)

Define as áreas da empresa e seus respectivos gerentes.

3. Avaliações (avaliacoes)

Registra notas periódicas de desempenho e feedbacks resumidos.

4. Benefícios (beneficios)

Armazena benefícios utilizados por cada funcionário (ex.: vale-alimentação, plano de saúde).

5. Usuários do Sistema (usuarios_sistema)

Controla autenticação, senhas e o papel de cada usuário no sistema (estagiário, analista, gerente, RH ou admin).

6. Logs de Acesso (logs_acesso)

Registra operações relevantes para auditoria, garantindo rastreabilidade.

🔐 Camadas de Acesso (views por papel)

O sistema utiliza views dedicadas, garantindo que cada tipo de usuário veja apenas o que faz sentido para seu papel:

Estagiário: apenas informações básicas de seu setor.

Analista: acesso limitado ao setor, com salários e avaliações anonimizados.

Gerente: visão completa de seu departamento, com dados reais e relatórios.

RH: acesso global às informações sensíveis.

Admin: gerencia permissões, papéis e auditoria.

Controle via GRANT/REVOKE diretamente no banco.

📊 Dashboards e BI

O sistema inclui visualizações de:

distribuição salarial

desempenho por setor

utilização de benefícios

evolução da força de trabalho

métricas agregadas com ruído via Privacidade Diferencial

Relatórios podem ser exportados em Excel.

🔒 Privacidade Diferencial

Aplicada em consultas estatísticas que expõem padrões agregados, evitando vazamento indireto de informações sensíveis.
O mecanismo utilizado (ex.: Laplace) é configurável conforme o nível de privacidade desejado.

📌 Relação com o Projeto B (Machine Learning)

Embora independente, o banco do Projeto A serve como base real para que o Projeto B explore:

ataques de inferência

vazamento de atributos

impactos de diferentes níveis de DP

O A é o "mundo real protegido".
O B é o ambiente de pesquisa que tenta ultrapassar essas proteções.
