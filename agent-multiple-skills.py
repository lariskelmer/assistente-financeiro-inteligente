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

from detectingfraud.scripts.profile_db_tool import get_user_behavioral_baseline
from explainpotentialfraud.scripts.database_query_transaction import get_transaction_from_db
from analyzecontext.scripts.context_analyzer import update_transaction_status

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
        os.getcwd(),
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
        os.getcwd(), 'detectingfraud')
)
explain_potential_fraud = load_skill_from_dir(
    os.path.join(
        os.getcwd(), 'explainpotentialfraud')
)
analyze_transaction_context_skill = load_skill_from_dir(
    os.path.join(
        os.getcwd(), 'analyzecontext')
)

my_skill_toolset = SkillToolset(
    skills=[detecting_fraud_skill,explain_potential_fraud,analyze_transaction_context_skill],
    code_executor=UnsafeLocalCodeExecutor(),
)

root_agent = Agent(
    model = "gemini-2.5-flash",
    name="skill_user_agent",
    description="""You are a credit card fraud detection concierge agent. Your job is to protect cardholders by analyzing transactions and communicating with them when needed.

You have access to three skills via the SkillToolset. ALWAYS load and follow the relevant skill before using any tool:

1. **detectingfraud** — Use when a raw transaction JSON payload is provided. Load this skill to evaluate whether the transaction is SUSPICIOUS or CONSISTENT against the cardholder's behavioral baseline.

2. **analyzecontext** — Use immediately after detectingfraud returns a SUSPICIOUS verdict. Load this skill to ask the user whether the flagged transaction was planned, an emergency, or fraud, then act accordingly.

3. **explainpotentialfraud** — Use when the user asks why a past transaction was flagged or wants to dispute a charge.

CRITICAL: Always call the 'load_skill' tool first to read the full SKILL.md instructions before executing any steps.""",
    tools=[
        my_skill_toolset,read_behavioral_rules,get_user_behavioral_baseline,get_transaction_from_db,update_transaction_status
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
    
    # user_prompt = """
    #     Explain to me why my transaction_id = 'tx_alex_11_f' was a Fraud ? I'm cardholder_id = 'user_1'.
    # """

    runner = InMemoryRunner(agent=root_agent)

    def read_multiline() -> str:
        """Reads until a blank line. Single-line input is sent immediately."""
        print("\nYou (press Enter twice to send):")
        lines = []
        while True:
            line = input()
            if line == "" and lines:
                break
            lines.append(line)
        return "\n".join(lines)

    while True:
        user_prompt = await asyncio.to_thread(read_multiline)

        if user_prompt.strip().lower() in ['exit', 'quit']:
            print("Ending session. Goodbye!")
            break

        if not user_prompt.strip():
            continue
            
        try:
            # 4. Send the input to the agent and await the response
            # Note: Depending on your specific ADK version, runner.run() or runner.run_debug() 
            # maintains conversational state across sequential calls.
            print("\n⏳ Analyzing...", flush=True)
            agent_response = await runner.run_debug(user_prompt, quiet=True)

            printed_any = False
            for event in agent_response:
                if not (hasattr(event, 'content') and event.content and event.content.parts):
                    continue
                text = "".join(
                    part.text for part in event.content.parts
                    if hasattr(part, 'text') and part.text
                )
                if text.strip():
                    print(f"\nAgent: {text}")
                    printed_any = True
            if not printed_any:
                print("\nAgent: [No text response returned]")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")    

    

        
if __name__ == '__main__':
    asyncio.run(main())