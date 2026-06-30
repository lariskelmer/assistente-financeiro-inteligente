# Assistente Financeiro Inteligente (Concierge Bancario)

Projeto final desenvolvido para a disciplina de Topicos Especiais, ministrada pelo Prof. Dr. Ivanovitch Silva.

Este repositorio contem a implementacao de um Assistente Financeiro Inteligente estruturado a partir de Sistemas Multi-Agentes e Large Language Models (LLMs). O sistema atua como um concierge bancario pro-ativo, projetado para transcender modelos tradicionais de perguntas e respostas (Q&A). O agente analisa transacoes em tempo real, detecta anomalias comportamentais e interage com o usuario para auxiliar em tomadas de decisao financeira estrategicas.

## Arquitetura do Sistema

O fluxo de decisao do assistente foi arquitetado em quatro camadas interligadas:

1. **Deteccao de Anomalias (Baseline e Regras):** O sistema estabelece um baseline comportamental baseado no historico de transacoes do usuario (ex: ultimos 30 a 90 dias). Durante a execucao, o agente avalia parametros granulares da transacao, como valor da compra, categoria do estabelecimento, localizacao geografica, tipo de terminal e a impressao digital do dispositivo (device fingerprint). Se uma transacao desvia do padrao (como um gasto significativamente acima da media daquela categoria), uma flag de seguranca e levantada.
2. **Analise de Contexto (Agente Conversacional):** Ao detectar uma anomalia, o agente investiga o racional da compra interagindo diretamente com o usuario. O sistema procura classificar se a transacao e fruto de um planejamento, uma emergencia ou se requer reconsideracao estrategica.
3. **Validacao Human-in-the-Loop:** O agente atua de forma consultiva e nao toma decisoes criticas isoladamente. Ele formula hipoteses e cenarios financeiros, exigindo que o usuario analise e valide as estrategias propostas, retroalimentando o sistema e treinando o grau de confianca (confidence score) para transacoes futuras.
4. **Analise Financeira e Roteamento:** Apos a elucidacao do contexto, o agente analisa de forma paralela diversos fluxos de informacao (fluxo de caixa, custos de juros, restricoes legais e limites de credito) para sugerir a melhor modalidade de pagamento ou mitigacao de danos.

## Modulos e Skills do Agente

O nucleo inteligente e composto por ferramentas modulares (Skills) que concedem capacidades especificas ao agente:

* **Avaliacao Comportamental (Fraud Detection):** Skill responsavel por cruzar os dados da transacao atual com o banco de dados simulado do usuario (ex: `assets/user_1.csv`). Identifica ocorrencias de violacao de velocidade (velocity violations), mudancas abruptas de canal e dimensionamento anomalos de ticket.
* **Simulacao de Opcoes de Pagamento:** Calcula as melhores alternativas de composicao de pagamento (ex: uso hibrido de recursos em conta e parcelamento) visando a reducao de juros.
* **Estimativa de Impacto Futuro:** Ferramenta focada em projetar como uma dada despesa e sua forma de pagamento afetarao a relacao divida/renda do usuario no longo prazo.

## Tecnologias e Ferramentas Utilizadas

* **Google ADK (Agent Development Kit):** Framework base adotado para a orquestracao, registro e teste do agente e suas skills.
* **Python:** Linguagem utilizada no desenvolvimento dos scripts locais de analise, simulacoes e integracao com bases de dados falsas (mock data).
* **LLMs:** Modelos fundacionais encarregados da inferencia semantica, avaliacao de regras complexas e interacao natural com o usuario.

## Membros da Equipe

* Larissa Kelmer de Menezes Silva
* Marilia Costa Muniz
* Samuel Amico Fidelis
