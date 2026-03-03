from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

def load_llm():
    llm = ChatOpenAI(model='Qwen3-4B-Instruct-2507', base_url="http://10.17.103.17:7000/v1",api_key=f"{os.getenv('VLLM_TOKEN')}")
    # llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', api_key=f"{os.getenv('GOOGLE_API_KEY')}")
    return llm
