# Assistente Financeiro Inteligente (Concierge Bancario)

Projeto final desenvolvido para a disciplina de Topicos Especiais, ministrada pelo Prof. Dr. Ivanovitch Silva[cite: 1].

Este repositorio contem a implementacao de um Assistente Financeiro Inteligente estruturado a partir de Sistemas Multi-Agentes e Large Language Models (LLMs)[cite: 1]. O sistema atua como um concierge bancario pro-ativo, projetado para transcender modelos tradicionais de perguntas e respostas (Q&A)[cite: 1]. O agente analisa transacoes em tempo real, detecta anomalias comportamentais e interage com o usuario para auxiliar em tomadas de decisao financeira estrategicas[cite: 2].

## Arquitetura do Sistema

O fluxo de decisao do assistente foi arquitetado em quatro camadas interligadas[cite: 2]:

1. **Deteccao de Anomalias (Baseline e Regras):** O sistema estabelece um baseline comportamental baseado no historico de transacoes do usuario (ex: ultimos 30 a 90 dias)[cite: 2]. Durante a execucao, o agente avalia parametros granulares da transacao, como valor da compra, categoria do estabelecimento, localizacao geografica, tipo de terminal e a impressao digital do dispositivo (device fingerprint)[cite: 1]. Se uma transacao desvia do padrao (como um gasto significativamente acima da media daquela categoria), uma flag de seguranca e levantada[cite: 2].
2. **Analise de Contexto (Agente Conversacional):** Ao detectar uma anomalia, o agente investiga o racional da compra interagindo diretamente com o usuario[cite: 2]. O sistema procura classificar se a transacao e fruto de um planejamento, uma emergencia ou se requer reconsideracao estrategica[cite: 2].
3. **Validacao Human-in-the-Loop:** O agente atua de forma consultiva e nao toma decisoes criticas isoladamente[cite: 2]. Ele formula hipoteses e cenarios financeiros, exigindo que o usuario analise e valide as estrategias propostas, retroalimentando o sistema e treinando o grau de confianca (confidence score) para transacoes futuras[cite: 2].
4. **Analise Financeira e Roteamento:** Apos a elucidacao do contexto, o agente analisa de forma paralela diversos fluxos de informacao (fluxo de caixa, custos de juros, restricoes legais e limites de credito) para sugerir a melhor modalidade de pagamento ou mitigacao de danos[cite: 2].

## Modulos e Skills do Agente

O nucleo inteligente e composto por ferramentas modulares (Skills) que concedem capacidades especificas ao agente:

* **Avaliacao Comportamental (Fraud Detection):** Skill responsavel por cruzar os dados da transacao atual com o banco de dados simulado do usuario (ex: `assets/user_1.csv`)[cite: 1]. Identifica ocorrencias de violacao de velocidade (velocity violations), mudancas abruptas de canal e dimensionamento anomalos de ticket[cite: 1].
* **Simulacao de Opcoes de Pagamento:** Calcula as melhores alternativas de composicao de pagamento (ex: uso hibrido de recursos em conta e parcelamento) visando a reducao de juros[cite: 2].
* **Estimativa de Impacto Futuro:** Ferramenta focada em projetar como uma dada despesa e sua forma de pagamento afetarao a relacao divida/renda do usuario no longo prazo[cite: 2].

## Tecnologias e Ferramentas Utilizadas

* **Google ADK (Agent Development Kit):** Framework base adotado para a orquestracao, registro e teste do agente e suas skills[cite: 1].
* **Python:** Linguagem utilizada no desenvolvimento dos scripts locais de analise, simulacoes e integracao com bases de dados falsas (mock data)[cite: 1].
* **LLMs:** Modelos fundacionais encarregados da inferencia semantica, avaliacao de regras complexas e interacao natural com o usuario[cite: 1].

## Membros da Equipe

* Larissa Kelmer de Menezes Silva[cite: 1]
* Marilia Costa Muniz[cite: 1]
* Samuel Amico Fidelis[cite: 1]
