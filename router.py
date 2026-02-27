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
Notes:
- If the user message is not related to any of the domains, return "chitchat"
- Use the conversation context to understand follow-up messages. For example, if the assistant asked for a customer ID and the user replies with a number, classify it based on the ongoing conversation topic.
Return JSON:
{"domain": "..."}
"""

def detect_route(message: str, context: list = None) -> str:
    prompt = "Instructions: \n" + route_prompt

    if context:
        prompt += "\nRecent conversation:\n"
        for msg in context:
            prompt += f"- {msg['role']}: {msg['content']}\n"

    prompt += "\nUser message:\n" + message

    response = llm.invoke(prompt)

    try:
        data = json.loads(response.content)
        return data.get("domain", "chitchat")
    except Exception as e:
        return f"Error: {e}"