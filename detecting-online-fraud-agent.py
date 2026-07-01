import json
import os
import pandas as pd
import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.adk import Agent
from google.adk.code_executors.unsafe_local_code_executor import UnsafeLocalCodeExecutor
from google.adk.skills import load_skill_from_dir
from google.adk.skills import models
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.skill_toolset import SkillToolset
from google.genai import types

from detectingfraud.scripts.profile_db_tool import get_user_behavioral_baseline

# Load the variables from the .env file into the environment
load_dotenv(os.path.join(
    os.getcwd(), '.env'
))

def read_behavioral_rules() -> str:
    """
    Reads the baseline threshold decision rules for velocity and channel anomalies.
    Use this whenever you need to reference fraud detection rules.
    """
    rules_path = os.path.join(
        "/Users/samico/Documents/DOUTORADO/PPGEEC-Transformer,Agents/Projeto06/concier_agent",
        "detectingfraud", 
        "references", 
        "behavioral_rules.md"
    )
    if os.path.exists(rules_path):
        with open(rules_path, "r") as f:
            return f.read()
    return "Error: behavioral_rules.md file could not be found on disk."


## Load Skill
detecting_fraud_skill = load_skill_from_dir(
    os.path.join(
        '/Users/samico/Documents/DOUTORADO/PPGEEC-Transformer,Agents/Projeto06/concier_agent', 'detectingfraud')
)

# WARNING: UnsafeLocalCodeExecutor has security concerns and should NOT
# be used in production environments.
my_skill_toolset = SkillToolset(
    skills=[detecting_fraud_skill],
    code_executor=UnsafeLocalCodeExecutor(),
)

root_agent = Agent(
    model = "gemini-2.5-flash",
    name="skill_user_agent",
    description="""An agent that helps user to know the transactions made by their credit card. You have access to specialized folder-based skills
        CRITICAL: Always use the 'load_skill' tool to read the skill instructions (SKILL.md) 
        completely before attempting to use any references or script execution tools.""",
    tools=[
        my_skill_toolset,read_behavioral_rules,get_user_behavioral_baseline
    ],
)

print("\n --- ADK REGISTRATION DEBUGGER ---")
print(f"Agent Name: {root_agent.name}")
print("Registered Tools List:")
for tool in root_agent.tools:
    # This prints the actual function names ADK registered
    print(f" {tool}")
print("------------------------------------\n")

def get_user_streaming_transaction(user_id: str) -> list:
    """
    """
    root_folder = os.getcwd()
    filepath = os.path.join(root_folder, 'data', 'log_transactions.json')
    with open(filepath, 'r') as file:
        streaming_data_json = json.load(file)
        
    user_streaming_json = streaming_data_json[user_id]
    
    return user_streaming_json


def ack_transaction_db(user_id: str, transaction_event: dict,is_fraud_flag:bool) -> None:
    """
    """
    root_folder = os.getcwd()
    filepath = os.path.join(root_folder, 'detectingfraud/assets', f'{user_id}.csv')
    print("="*30)
    print('\n\n\n')
    print(f"Adding Transaction to the DB \n")
    df = pd.read_csv(filepath)
    #-- Parser the Transaction

    
    new_transaction_df = pd.DataFrame({
        'transaction_id': [transaction_event.get('transaction_id')],
        'timestamp': [transaction_event.get('timestamp')],
        'amount': [transaction_event.get('amount')],
        'currency': [transaction_event.get('currency')],
        'merchant_name': [transaction_event.get('merchant').get('name')],
        'merchant_category': [transaction_event.get('merchant').get('category')],
        'location_city': [transaction_event.get('location').get('city')],
        'location_country': [transaction_event.get('location').get('country')],
        'terminal_type': [transaction_event.get('location').get('terminal_type')],
        'vpn_detected': [transaction_event.get('network').get('vpn_detected')],
        'device_fingerprint': [transaction_event.get('device').get('device_fingerprint')],
        'is_fraud': [is_fraud_flag],
    })
    print(f"Commit Transaction to the DB \n")
    print("="*30)
    print('\n\n\n')
    df_new = pd.concat([df,new_transaction_df],ignore_index=True)
    df_new.to_csv(filepath,index=False)

async def main():
    streaming_evets = get_user_streaming_transaction('user_1')
    #--- Streaming of transaction events
    for event in streaming_evets:
        # Call Agent
        is_fraud_flag = event.get('comment','')
        is_fraud_flag = True if is_fraud_flag != '' else False
        event['comment'] = 'empty'
        
        prompt = f"""Transaction for cardholder_id = user_1: \n {event} \n"""
        print("="*30)
        print('\n\n')
        print(prompt)
        print("="*30)
        print('\n\n')
        runner = InMemoryRunner(agent=root_agent)
        agent_response = await runner.run_debug(prompt)

        # # Save Agent response into a txt
        # final_text = "".join(str(agent_response))
        # final_text = final_text.join(f"FRAUD = {event.get('comment','NOT FRAUD')}")

        # output_dir = os.path.join(os.getcwd(),'data')
        # output_file_path = os.path.join(output_dir, "user_1_agent_response.txt")

        # with open(output_file_path, "w", encoding="utf-8") as txt_file:
        #     txt_file.write(final_text)

        # print(f"\n\n Agent response successfully saved to: {output_file_path}")
        
        # Add the new transaction to the data
        print("="*30)
        print(f"\n FRAUD OR NOT: {is_fraud_flag} \n")
        print("="*30)
        
        ack_transaction_db(user_id='user_1',transaction_event=event,is_fraud_flag=is_fraud_flag)
        
if __name__ == '__main__':
    asyncio.run(main())