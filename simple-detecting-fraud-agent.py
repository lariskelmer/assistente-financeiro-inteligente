import os
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

# Load the variables from the .env file into the environment
load_dotenv(os.path.join(
    os.getcwd(), '.env'
))

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
        my_skill_toolset,read_behavioral_rules
    ],
)


print("\n --- ADK REGISTRATION DEBUGGER ---")
print(f"Agent Name: {root_agent.name}")
print("Registered Tools List:")
for tool in root_agent.tools:
    # This prints the actual function names ADK registered
    print(f" {tool}")
print("------------------------------------\n")


async def main():
    query_example: str = """
        {
            "transaction_id": "tx_alex_01",
            "timestamp": "2026-06-20T08:12:00Z",
            "cardholder_id": "user_1",
            "amount": 14.99,
            "currency": "USD",
            "merchant": { "name": "Netflix Inc", "category": "STREAMING", "id": "m_net_88" },
            "location": { "city": "Seattle", "country": "US", "terminal_type": "ONLINE" },
            "network": { "ip_address": "67.180.20.44", "vpn_detected": false, "proxy_detected": false },
            "device": { "device_fingerprint": "mac_safari_991", "os": "MacOS", "browser_or_app": "Safari" },
            "payment_details": { "cvv_validated": true, "emv_fallback": false }
        }
    """
    runner = InMemoryRunner(agent=root_agent)
    events = await runner.run_debug(query_example)
    
    
if __name__ == '__main__':
    asyncio.run(main())