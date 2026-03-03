from langchain.agents import create_agent
from MCP.tech.mcp import check_ont, restart_ont
from MCP.tech.sys_prompt import system_prompt
from llm import load_llm


tools = [check_ont, restart_ont]

def run(user_msg:str, chat_history: list):
    formatted_history = "\n".join([f"{msg['role'].upper()}: {msg.get('message', msg.get('content', ''))}" for msg in chat_history])
    dynamic_prompt = system_prompt() + f"\n\n--- THIS IS SAVED MEMORY CONSERVATION. IF USER ASKED TO DO SOMETHING OR MAKE SOMETHING, MAKE SURE TO READ USER ID FROM THIS MEMORY ---\n{formatted_history}"
    agent = create_agent(model=load_llm(), tools=tools, system_prompt=dynamic_prompt)
    return agent.invoke({"messages": user_msg})
