---
name: detectingfraud
description: Use this skill when a new credit card transaction is received to evaluate it using the user's historical transaction patterns.
metadata:
  author: samuel
  version: "1.0"
  adk_additional_tools:
    - profile_db_tool
---

Step 0: All the necessary files are under the folder detectingfraud, so please read from this folder first and them you can access assets, reference and scripts
Step 1: Parse the incoming transaction JSON payload to extract the `cardholder_id`.
Step 2: Run the `read_behavioral_rules` tool to review the baseline threshold decision rules for velocity and channel anomalies.
Step 3: Run the `scripts/profile_db_tool` function get_user_behavioral_baseline with the extracted `cardholder_id` to retrieve a markdown text that contain stats information about historical transactions from the `cardholder_id`.
Step 4: Compare the current transaction metrics (amount, location, terminal type, device) against the historical profile data.
Step 5: Provide a structured evaluation using the exact formatting below:

### Behavioral Assessment
* **Verdict:** [SUSPICIOUS | CONSISTENT]
* **Confidence Rating:** [0-100]
* **Analytical Summary:** [Detailed explanation citing historical stats vs. new transaction metrics]

Step 6: If the Verdict is SUSPICIOUS, do not take a final action yet. Hand off to the `analyzecontext` skill, passing the `transaction_id`, `amount`, `category`, and the reason for the flag, so the user can be asked for context (Human-in-the-Loop) before the transaction is authorized, blocked, or re-routed.