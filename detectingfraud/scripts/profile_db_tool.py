import os
import pandas as pd
from typing import Dict, Any

def get_user_behavioral_baseline(cardholder_id: str) -> str:
    """
    Retrieves the historical transaction baseline for a specific cardholder.

    Args:
        cardholder_id (str): The unique identifier of the cardholder (e.g., 'user_q').

    Returns:
        str: A markdown formatted summary of the user's last 10 valid transactions and spending habits.
    """
    # Safeguard pathing relative to execution roots
    base_dir = os.path.join(os.getcwd(),'detectingfraud') #'/Users/samico/Documents/DOUTORADO/PPGEEC-Transformer,Agents/Projeto06/concier_agent/detectingfraud' #
    file_path = os.path.join(base_dir, "assets", f"{cardholder_id}.csv")
    
    print(file_path)
    if not os.path.exists(file_path):
        return f"Error: No historical profile baseline records found for user '{cardholder_id}'."
    
    try:
        df = pd.read_csv(file_path)
        
        # Split history contextually
        normal_tx = df[df['is_fraud'] == False].tail(10)
        past_frauds = df[df['is_fraud'] == True]
        
        # Build statistical features
        avg_spend = normal_tx['amount'].mean()
        max_spend = normal_tx['amount'].max()
        top_categories = normal_tx['merchant_category'].mode().tolist()
        fav_cities = normal_tx['location_city'].unique().tolist()
        channels = normal_tx['terminal_type'].unique().tolist()
        
        summary = (
            f"=== BEHAVIORAL PROFILE FOR {cardholder_id} ===\n"
            f"Historical Average Ticket Size: ${avg_spend:.2f}\n"
            f"Maximum Historical Ticket Size: ${max_spend:.2f}\n"
            f"Frequent Merchant Verticals: {', '.join(top_categories)}\n"
            f"Established Safe Locations: {', '.join(fav_cities)}\n"
            f"Utilized Terminal Types: {', '.join(channels)}\n"
            f"Prior Fraud Incidents on Account: {len(past_frauds)} detected historically.\n\n"
            f"=== LAST 10 VALID TRANSACTIONS ===\n"
            f"{normal_tx.to_markdown(index=False)}\n"
        )
        return summary
    except Exception as e:
        print(e)
        return f"Error compiling database profiling indexes: {str(e)}"