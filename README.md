# Concierge Bancário — Assistente Financeiro Inteligente

> Projeto final da disciplina **Tópicos Especiais em Redes**, ministrada pelo Prof. Dr. Ivanovitch Silva — PPGEEC/UFRN.

Sistema de agente único com múltiplas skills que detecta fraudes em transações de cartão de crédito, interage com o portador para validação Human-in-the-Loop e explica decisões históricas, utilizando Google ADK e Gemini.

---

## Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Skills](#skills)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Perfis de Teste](#perfis-de-teste)
- [Equipe](#equipe)

---

## Visão Geral

O Concierge Bancário é um agente conversacional pro-ativo que vai além do modelo tradicional de Q&A. Em vez de apenas responder perguntas, ele:

1. **Detecta anomalias** em tempo real comparando cada transação com o baseline comportamental do portador.
2. **Interage com o usuário** (Human-in-the-Loop) quando uma transação é sinalizada, pedindo contexto antes de qualquer ação.
3. **Explica e audita** decisões passadas quando o portador questiona uma cobrança.

A arquitetura segue o padrão **Harness**: um único agente central equipado com skills modulares (Skills + Memória + Protocolos), conforme descrito na literatura de sistemas agênticos.

---

## Arquitetura

```
Transação JSON / Pergunta do Usuário
              ↓
         [ Agent ]  ←──────────────────────────────────┐
              │                                         │
     ┌────────┴──────────┐                             │
     ▼                   ▼                             │
detectingfraud     explainpotentialfraud          analyzecontext
(nova transação)   (disputa histórica)            (HITL pós-SUSPICIOUS)
     │
     ├─ CONSISTENT → encerra
     └─ SUSPICIOUS → analyzecontext
                          │
               ┌──────────┼──────────┐
               ▼          ▼          ▼
           Autoriza    Bloqueia   Pede mais
                       cartão     contexto
```

| Diagrama | Descrição |
|---|---|
| [Agent_Skill_Fraud.png](draw/Agent_Skill_Fraud.png) | Visão geral do harness (Agent + Skills/Memória/Protocolos) |
| [Agent_Skill_Call.png](draw/Agent_Skill_Call.png) | Estrutura interna de uma skill (SKILL.md + assets + scripts + reference) |
| [Transaction_Trigger.png](draw/Transaction_Trigger.png) | Roteamento por tipo de entrada (transação vs. pergunta do usuário) |
| [Analyzecontext_Skill.png](draw/Analyzecontext_Skill.png) | Fluxo Human-in-the-Loop da skill `analyzecontext` |

---

## Skills

| Skill | Trigger | Responsabilidade | Tool principal |
|---|---|---|---|
| `detectingfraud` | Payload JSON de transação recebido | Compara métricas da transação com o histórico do portador e emite veredito SUSPICIOUS / CONSISTENT | `get_user_behavioral_baseline` |
| `analyzecontext` | Veredito SUSPICIOUS da `detectingfraud` | Pergunta ao portador se a transação foi planejada, emergência ou fraude; age conforme a resposta | `update_transaction_status` |
| `explainpotentialfraud` | Pergunta retrospectiva do usuário | Busca a transação histórica, cruza com as regras e explica o veredito em linguagem natural; pode remover a entrada do banco se fraude confirmada | `get_transaction_from_db` |

Cada skill é uma pasta independente contendo:

```
<skill>/
├── SKILL.md          # instruções para o LLM (when to use, workflow, examples)
├── assets/           # dados mock por usuário (CSV)
├── references/       # regras de negócio (behavioral_rules.md)
└── scripts/          # ferramentas Python registradas no agente
```

---

## Pré-requisitos

- Python 3.11+
- Chave de API do Google Gemini (`GOOGLE_API_KEY`)

---

## Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repo>
cd concier_agent

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
# Edite o arquivo .env com sua chave:
# GOOGLE_API_KEY="sua-chave-aqui"
# GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

---

## Uso

```bash
python agent-multiple-skills.py
```

O terminal aguarda input. **Pressione Enter duas vezes** para enviar (suporta JSON multilinha).

### Exemplos de teste

**Detectar fraude em transação nova** (deve retornar SUSPICIOUS e acionar `analyzecontext`):
```
Evaluate this transaction for fraud: {"transaction_id": "tx_alex_11_f", "cardholder_id": "user_1", "amount": 1299.00, "merchant": {"name": "Apple Store", "category": "ELECTRONICS"}, "location": {"city": "Miami", "country": "US", "terminal_type": "EMV_FALLBACK"}, "network": {"ip_address": "0.0.0.0", "vpn_detected": false, "proxy_detected": false}, "device": {"device_fingerprint": "none", "os": "none"}, "payment_details": {"cvv_validated": false, "emv_fallback": true}}
```

**Transação legítima** (deve retornar CONSISTENT sem acionar `analyzecontext`):
```
Evaluate this transaction for fraud: {"transaction_id": "tx_alex_01", "cardholder_id": "user_1", "amount": 14.99, "merchant": {"name": "Netflix Inc", "category": "STREAMING"}, "location": {"city": "Seattle", "country": "US", "terminal_type": "ONLINE"}, "network": {"ip_address": "67.180.20.44", "vpn_detected": false, "proxy_detected": false}, "device": {"device_fingerprint": "mac_safari_991", "os": "MacOS"}, "payment_details": {"cvv_validated": true, "emv_fallback": false}}
```

**Explicar transação histórica** (`explainpotentialfraud`):
```
Explain to me why my transaction_id = 'tx_alex_11_f' was considered fraud. I'm cardholder_id = 'user_1'.
```

---

## Estrutura do Projeto

```
concier_agent/
├── agent-multiple-skills.py        # ponto de entrada principal (CLI interativo)
├── requirements.txt
├── .env                            # GOOGLE_API_KEY (não versionar)
│
├── detectingfraud/                 # Skill 1 — detecção de anomalias
│   ├── SKILL.md
│   ├── assets/                     # histórico de transações por usuário
│   │   ├── user_1.csv  (Alex — perfil digital)
│   │   ├── user_2.csv  (Bob  — perfil físico/conservador)
│   │   ├── user_3.csv  (Clara — perfil familiar)
│   │   └── user_4.csv  (David — perfil de rotina)
│   ├── references/
│   │   └── behavioral_rules.md     # regras de velocity e anomalia de canal
│   └── scripts/
│       └── profile_db_tool.py      # get_user_behavioral_baseline()
│
├── analyzecontext/                 # Skill 2 — validação Human-in-the-Loop
│   ├── SKILL.md
│   └── scripts/
│       └── context_analyzer.py     # update_transaction_status()
│
├── explainpotentialfraud/          # Skill 3 — auditoria e disputa
│   ├── SKILL.md
│   ├── assets/                     # mesmos CSVs (visão da skill de disputa)
│   ├── references/
│   │   └── behavioral_rules.md
│   └── scripts/
│       └── database_query_transaction.py  # get_transaction_from_db(), delete_transaction_from_db()
│
├── data/
│   └── log_transactions.json       # payloads de teste (15 transações por usuário, 5 fraudulentas)
│
├── draw/                           # diagramas de arquitetura
│   ├── Agent_Skill_Fraud.png
│   ├── Agent_Skill_Call.png
│   ├── Transaction_Trigger.png
│   └── Analyzecontext_Skill.png
│
└── Agent_Pipeline.ipynb            # notebook de exploração e prototipagem
```

---

## Perfis de Teste

O arquivo `data/log_transactions.json` contém 4 perfis sintéticos, cada um com 10 transações legítimas e 5 fraudes de dificuldade crescente:

| ID | Perfil | Estratégia de fraude |
|---|---|---|
| `user_1` | Alex — heavy e-commerce, multi-device | Credential stuffing + card testing (micro → spike) |
| `user_2` | Bob — conservador, só ATM/POS em Omaha | Qualquer transação online ou internacional |
| `user_3` | Clara — mãe de família, gastos previsíveis | Compras fora do paradigma familiar (gaming, viagens) |
| `user_4` | David — rotina absoluta, Apple Pay exclusivo | Qualquer portal online sem tokenização NFC |

---

## Equipe

| Nome | Papel |
|---|---|
| **Larissa Kelmer de Menezes Silva** | Skill `analyzecontext` (Human-in-the-Loop) |
| **Marilia Costa Muniz** | Integração, testes e apresentação |
| **Samuel Amico Fidelis** | Arquitetura do harness, skills `detectingfraud` e `explainpotentialfraud` |

---

> Disciplina: Tópicos Especiais em Redes — PPGEEC/UFRN
> Orientador: Prof. Dr. Ivanovitch Silva
