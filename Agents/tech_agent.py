from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from MCP.tech.mcp import create_ticket, find_user, create_user
from MCP.tech.sys_prompt import system_prompt
from llm import load_llm


tools = [create_ticket, find_user, create_user]

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt()),
    ("placeholder", "{chat_history}"),
    ("human", "{input}")
])

agent = create_agent(model=load_llm(), tools=tools)

