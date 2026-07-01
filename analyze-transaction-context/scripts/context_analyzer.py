import json

def parse_user_intent(user_response: str) -> str:
    """
    Simula a orquestração do LLM para classificar a resposta do usuário.
    Em um ambiente real de orquestração, isso seria um prompt de classificação.
    """
    response_lower = user_response.lower()
    
    if any(word in response_lower for word in ["fraude", "não reconheço", "golpe", "desconheço", "clonaram"]):
        return "FRAUD_CONFIRMED"
    elif any(word in response_lower for word in ["emergência", "urgente", "hospital", "acidente"]):
        return "EMERGENCY"
    elif any(word in response_lower for word in ["sim", "fui eu", "planejado", "trabalho", "comprei"]):
        return "PLANNED_EXPENSE"
    else:
        return "NEEDS_CLARIFICATION"

def update_transaction_status(transaction_id: str, user_response: str) -> str:
    """
    Função principal da skill que avalia o contexto do usuário e define o próximo passo.
    """
    intent = parse_user_intent(user_response)
    
    # Simulação de atualização no banco de dados (mock)
    log_entry = {
        "transaction_id": transaction_id,
        "user_feedback": user_response,
        "classified_intent": intent,
        "action_taken": ""
    }
    
    if intent == "FRAUD_CONFIRMED":
        log_entry["action_taken"] = "BLOCK_AND_REFUND"
        result_msg = f"Ação Crítica: Transação {transaction_id} bloqueada com sucesso por suspeita de fraude. Cartão virtual cancelado."
        
    elif intent == "EMERGENCY" or intent == "PLANNED_EXPENSE":
        log_entry["action_taken"] = "ROUTE_TO_FINANCIAL_ANALYSIS"
        result_msg = f"Transação reconhecida como '{intent}'. Recomenda-se acionar a skill de análise de fluxo de caixa para sugerir opções de pagamento (ex: FGTS, parcelamento)."
        
    else:
        log_entry["action_taken"] = "PROMPT_USER_AGAIN"
        result_msg = "Não foi possível compreender o contexto. Por favor, solicite ao usuário que seja mais específico."

    # Aqui você salvaria o log_entry no seu user_1.csv ou transaction.log
    # print(json.dumps(log_entry, indent=2))
    
    return result_msg

# Exemplo de teste local rápido:
# if __name__ == "__main__":
#     print(update_transaction_status("tx_alex_02", "fui eu sim, comprei pra trabalhar"))