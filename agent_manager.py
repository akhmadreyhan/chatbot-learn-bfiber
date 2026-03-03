from Agents import tech_agent
# from Agents.billing_agent import agent as billing_agent
from Agents import sales_agent
# from Agents.faq_agent import agent as faq_agent

def get_agent(domain:str):
    if domain == "ont agent":
        return tech_agent
    # elif domain == "billing":
    #     return billing_agent
    elif domain == "sales order agent":
        return sales_agent
    # elif domain == "faq":
    #     return faq_agent
    else:
        return None