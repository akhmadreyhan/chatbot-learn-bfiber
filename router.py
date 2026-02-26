from llm import load_llm
import json


llm = load_llm()

route_prompt = """
Classify the user message into one domain:
- technical
- billing
- sales
- faq
Clues:
- technical: user message is related to technical issues, such as internet connection, speed, device, etc.
- billing: user message is related to billing issues, such as payment, invoice, subscription, etc.
- sales: user message is related to sales issues, such as new plan, upgrade, downgrade, etc.
- faq: user message is related to frequently asked questions, such as how to, what is, etc.
Notes: if the user message is not related to any of the domains, return "chitchat"
Return JSON:
{"domain": "..."}
"""

def detect_route(message:str) -> str:
    response = llm.invoke("Instructions: \n" +route_prompt + "\n User message:\n" + message)
    return response.content
    # try:
    #     data = json.loads(response.content)
    #     return data["domain"]
    # except:
    #     return "chitchat"