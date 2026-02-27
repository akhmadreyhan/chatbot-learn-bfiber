from langchain.agents import create_agent
from MCP.tech.mcp import so_get_profile, cn_cek_gangguan_masal, cn_cek_status_service, cn_cek_ip_dapat, cn_cek_session_pppoe, cn_trace_jalur
from MCP.tech.sys_prompt import system_prompt
from llm import load_llm


tools = [so_get_profile, cn_cek_gangguan_masal, cn_cek_status_service, cn_cek_ip_dapat, cn_cek_session_pppoe, cn_trace_jalur]

def run(user_msg:str, chat_history):
    agent = create_agent(model=load_llm(), tools=tools, system_prompt=system_prompt())
    return agent.invoke({"messages" : user_msg, "chat_history" : chat_history})
