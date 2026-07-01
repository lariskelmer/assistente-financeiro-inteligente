---
name: analyze-transaction-context
description: Use this skill when a credit card transaction is flagged as SUSPICIOUS by the fraud detection system, and you need to interact with the user to understand the context (e.g., planned expense, emergency, or actual fraud) before taking a final action.
metadata:
  author: larissa
  version: "1.0"
  adk_additional_tools:
    - update_transaction_status
---

## When to use
- Immediately after a transaction is classified as SUSPICIOUS or flagged for review by the behavioral assessment.
- When the system requires explicit human validation (Human-in-the-Loop) to decide whether to authorize, block, or re-route a transaction to financing options.

## When NOT to use
- Do not use for transactions already classified as CONSISTENT.
- Do not use to fetch historical data or behavioral rules (use the detectingfraud skill instead).

## Workflow
1. **Context Initialization:** Receive the `transaction_id`, `amount`, `category`, and the reason for the flag (e.g., "500% above baseline").
2. **User Interaction:** Prompt the user clearly about the anomaly. Ask if the transaction is: a) Planned/Expected, b) An Emergency, or c) Unrecognized/Fraud.
3. **Intent Parsing:** Analyze the user's natural language response using the LLM to map it to one of the three categories.
4. **Decision Logic:**
   - If **Unrecognized/Fraud**: Instruct the agent to escalate immediately to blocking the card and reversing the charge.
   - If **Emergency** or **Planned**: Validate if the user has enough balance. If the amount impacts their financial health, gracefully suggest routing to the `calculate_payment_options` skill.
5. **Update Record:** Run the `update_transaction_status` tool to log the user's feedback and the agent's final decision into the mock database, training the baseline for future context.

## Examples
- **Input:** "The transaction tx_alex_01 for $1500 at 'TechStore' was flagged as SUSPICIOUS. Ask the user for context."
- **Output:** "I noticed an unusual charge of $1500 at TechStore. Could you confirm if this was a planned purchase, an emergency, or if you don't recognize this charge?"