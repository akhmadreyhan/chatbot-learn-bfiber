from langchain.agents import create_agent
from MCP.sales.mcp import so_get_profile, ubah_paket_langganan, pindah_alamat, bayar_tagihan, berhenti_langganan, mau_langganan, aktifkan_ulang_langganan, update_data_pelanggan
from MCP.sales.sys_prompt import system_prompt
from llm import load_llm


tools = [so_get_profile, ubah_paket_langganan, pindah_alamat, bayar_tagihan, berhenti_langganan, mau_langganan, aktifkan_ulang_langganan, update_data_pelanggan]

def run(user_msg:str, chat_history):
    agent = create_agent(model=load_llm(), tools=tools, system_prompt=system_prompt())
    return agent.invoke({"messages" : user_msg, "chat_history" : chat_history})
