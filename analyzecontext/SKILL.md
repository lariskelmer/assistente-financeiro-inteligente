---
name: analyzecontext
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
1. **Context Initialization:** Receive `transaction_id`, `amount`, `category`, and the reason for the flag (e.g., "500% above baseline") from the detectingfraud skill output.
2. **User Interaction:** Present the anomaly clearly to the user. Ask whether the transaction was: a) Planned/Expected, b) An Emergency, or c) Unrecognized/Fraud.
3. **Intent Parsing:** Analyze the user's natural language response and map it to one of the three categories above.
4. **Decision — Fraud Confirmed:** Call `update_transaction_status` with action `BLOCK_AND_REFUND`. Inform the user the card has been blocked immediately and a refund has been initiated.
5. **Decision — Emergency or Planned:** Call `update_transaction_status` with action `ROUTE_TO_FINANCIAL_ANALYSIS`. Confirm the transaction is authorized and suggest payment options (e.g., installments) if the amount is high.
6. **Decision — Needs Clarification:** Call `update_transaction_status` with action `PROMPT_USER_AGAIN`. Ask the user to be more specific before taking any action. Do not block or authorize yet.
7. **Update Record:** The result of `update_transaction_status` is always logged into the mock database to retrain the behavioral baseline for future transactions.

## Examples

**Scenario 1 — Flagging the transaction:**
- **Input:** "The transaction tx_alex_11_f for $1,299.00 at 'Apple Store' was flagged as SUSPICIOUS. The terminal was EMV_FALLBACK in Miami, outside the user's usual pattern."
- **Output:** "I noticed an unusual charge of $1,299.00 at Apple Store in Miami. Could you confirm: was this a planned purchase, an emergency, or do you not recognize this charge?"

**Scenario 2 — Fraud confirmed:**
- **Input (user response):** "I don't recognize this charge, it wasn't me."
- **Output:** "Understood. Since you don't recognize this transaction, we have taken the following actions: your card has been blocked immediately and a refund of $1,299.00 has been initiated. You will receive a confirmation shortly."

**Scenario 3 — Transaction recognized:**
- **Input (user response):** "Yes, I planned this purchase, it was a birthday gift."
- **Output:** "Got it — transaction tx_alex_11_f confirmed as a planned purchase. No blocking action will be taken. Your feedback has been recorded to improve your behavioral baseline."

**Scenario 4 — Ambiguous response:**
- **Input (user response):** "I'm not sure, maybe it was my wife."
- **Output:** "I was unable to determine the context clearly. Could you confirm directly with your wife whether this purchase was authorized? No action has been taken yet while the transaction remains under review."
