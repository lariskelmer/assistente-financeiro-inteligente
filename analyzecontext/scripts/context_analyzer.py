import json


def parse_user_intent(user_response: str) -> str:
    response_lower = user_response.lower()

    if any(word in response_lower for word in ["fraude", "não reconheço", "golpe", "desconheço", "clonaram",
                                                "fraud", "don't recognize", "unrecognized"]):
        return "FRAUD_CONFIRMED"
    elif any(word in response_lower for word in ["emergência", "urgente", "hospital", "acidente",
                                                  "emergency", "urgent"]):
        return "EMERGENCY"
    elif any(word in response_lower for word in ["sim", "fui eu", "planejado", "trabalho", "comprei",
                                                  "yes", "planned", "i made", "i did", "mine"]):
        return "PLANNED_EXPENSE"
    else:
        return "NEEDS_CLARIFICATION"


def update_transaction_status(transaction_id: str, user_response: str) -> str:
    """
    Evaluates the user's context for a flagged transaction and returns the recommended action.

    Args:
        transaction_id: The ID of the SUSPICIOUS transaction.
        user_response: The user's natural language explanation of the transaction.

    Returns:
        A string describing the action taken (block, route to financing, or ask again).
    """
    intent = parse_user_intent(user_response)

    log_entry = {
        "transaction_id": transaction_id,
        "user_feedback": user_response,
        "classified_intent": intent,
        "action_taken": "",
    }

    if intent == "FRAUD_CONFIRMED":
        log_entry["action_taken"] = "BLOCK_AND_REFUND"
        result_msg = (
            f"Critical Action: Transaction {transaction_id} has been blocked due to confirmed fraud. "
            "The virtual card has been cancelled and a refund has been initiated."
        )

    elif intent in ("EMERGENCY", "PLANNED_EXPENSE"):
        log_entry["action_taken"] = "ROUTE_TO_FINANCIAL_ANALYSIS"
        result_msg = (
            f"Transaction {transaction_id} recognized as '{intent}'. "
            "Recommend routing to financial analysis to suggest payment options (e.g. installments)."
        )

    else:
        log_entry["action_taken"] = "PROMPT_USER_AGAIN"
        result_msg = (
            "Could not determine the context of this transaction. "
            "Please ask the user to be more specific about whether the charge was planned, an emergency, or unrecognized."
        )

    return result_msg
