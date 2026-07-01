import os
import pandas as pd
from typing import Dict, Any

def get_transaction_from_db(cardholder_id: str, transaction_id: str) -> str:
    """
    Retrieves the historical transaction baseline for a specific cardholder.

    Args:
        cardholder_id (str): The unique identifier of the cardholder (e.g., 'user_q').

    Returns:
        str: A markdown formatted summary of the user's last 10 valid transactions and spending habits.
    """
    # Safeguard pathing relative to execution roots
    base_dir = os.path.join(os.getcwd(),'explainpotentialfraud')
    file_path = os.path.join(base_dir, "assets", f"{cardholder_id}.csv")
    
    print(file_path)
    # if not os.path.exists(file_path):
    #     return f"Error: No historical profile baseline records found for user '{cardholder_id}'."
    print(f'Reading the transaction_id = {transaction_id}')
    try:
        df = pd.read_csv(file_path)
        df_filter = df[df['transaction_id'] == transaction_id]
        print(df_filter)
        # Build statistical features
        amount = df_filter['amount'].iloc[0]
        merchant_category = df_filter['merchant_category'].iloc[0]
        location_city = df_filter['location_city'].iloc[0]
        terminal_type = df_filter['terminal_type'].iloc[0]
        
        summary = (
            f"=== BEHAVIORAL PROFILE FOR {cardholder_id} ===\n"
            f"Amount: ${amount:.2f}\n"
            f"Merchant Category: {merchant_category}\n"
            f"City Location: {location_city}\n"
            f"Terminal Type: {terminal_type}\n"
        )
        return summary
    
    except Exception as e:
        print(e)
        return f"Error compiling database profiling indexes: {str(e)}"
    
def delete_transaction_from_db(cardholder_id: str, transaction_id: str):
    # Safeguard pathing relative to execution roots
    base_dir = os.path.join(os.getcwd(),'explainpotentialfraud')
    file_path = os.path.join(base_dir, "assets", f"{cardholder_id}.csv")
    
    print(file_path)
    # if not os.path.exists(file_path):
    #     return f"Error: No historical profile baseline records found for user '{cardholder_id}'."
    print(f'Reading the transaction_id = {transaction_id}')
    try:
        df = pd.read_csv(file_path)
        df_filter = df[df['transaction_id'] != transaction_id]
        
        df_filter.to_csv(os.path.join(base_dir, "assets", f"{cardholder_id}_updated.csv"),index=False)
        summary = (
            f"Deleted transactionId = {transaction_id} Successfully"
        )
        return summary
    
    except Exception as e:
        print(e)
        return f"Error compiling database profiling indexes: {str(e)}"