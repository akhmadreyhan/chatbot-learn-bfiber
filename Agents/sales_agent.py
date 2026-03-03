from langchain.agents import create_agent
from MCP.sales.mcp import validate_customer, check_billing, check_gamas, get_ticket, create_escalation
from MCP.sales.sys_prompt import system_prompt
from llm import load_llm


# List the imported functions precisely matching the ones in your new MCP.sales.mcp file
tools = [validate_customer, check_billing, check_gamas, get_ticket, create_escalation]

def run(user_msg: str, chat_history: list):
    formatted_history = "\n".join([f"{msg['role'].upper()}: {msg.get('message', msg.get('content', ''))}" for msg in chat_history])
    print(formatted_history)
    dynamic_prompt = system_prompt() + f"\n\n--- THIS IS SAVED MEMORY CONSERVATION. IF USER ASKED TO DO SOMETHING OR MAKE SOMETHING, MAKE SURE TO READ USER ID FROM THIS MEMORY ---\n{formatted_history}"
    
    agent = create_agent(model=load_llm(), tools=tools, system_prompt=dynamic_prompt)
    return agent.invoke({"messages": user_msg})