---
name: explainpotentialfraud
description: Use this skill when a user asks for an explanation regarding why a credit card transaction was accepted or blocked, or when they request to dispute, flag, or revoke a past transaction due to fraud suspicion.
metadata:
  author: samuel
  version: "1.0"
---

## When to use
- When the user inquiries about the safety classification, block status, or non-detection of fraud on a specific historical transaction.
- When the user explicitly requests to review or dispute a charge they believe is fraudulent.

## When NOT to use
- Do not use for creating, staging, or executing new financial transactions.
- Do not use for checking raw, unprocessed transaction JSON payloads against general fraud parameters (use the syntax evaluation tool instead).
- Do not use for general bank account inquiries unrelated to specialized transaction review.

## Workflow
1. **Extract Identifiers:** Detect the `transaction_id` and `cardholder_id` from the context. If either is missing, explicitly prompt the user to provide them before continuing.
2. **Review System Rules:** Execute the `read_behavioral_rules` tool to evaluate the baseline threshold velocity and communication channel anomaly rules.
3. **Fetch Transaction Data:** Run the function `get_transaction_from_db` from the script `scripts/database_query_transaction.py` utilizing the confirmed `transaction_id` to filter the data and `cardholder_id` to get the file name.
4. **Analyze Cardholder History:** Call the `get_user_behavioral_baseline` function from `scripts/profile_db_tool` using the `cardholder_id` to evaluate historical behavioral metrics.
5. **Evaluate & Determine:** Cross-reference the transaction history against the rules. If the transaction was not originally marked as fraud, evaluate the user's specific context and arguments against the baseline.
6. **Action - Fraud Confirmed:** If the transaction matches fraud parameters or the user's justification exposes a confirmed security vulnerability, purge the entry from the database by running the function `delete_transaction_from_db` from `scripts/database_query_transaction.py` with the `transaction_id` and `cardholder_id`. Inform the user of the successful remediation.
7. **Action - Fraud Denied:** If the verification fails to confirm fraud, explicitly inform the user that the record cannot be deleted via this automated pathway. Instruct them to escalate the dispute by calling the central bank phone line directly, then gracefully close the inquiry.

## Examples
- **Input:** "Why my transaction_id: 'tx_h_bob_01' was not considered a fraud, my id is `user_2` ?"
- **Output:** "Based on the transaction evaluation rules and your historical transaction baseline, this charge fell within your typical spending parameters because..."