import json
from tools import list_tools, get_tool

def get_system_prompt():
    """Get the system prompt for the agent."""
    tools_list = "\n".join([f"- {name}" for name in list_tools()])
    
    return f"""You are a helpful AI assistant that can use tools to answer questions.

Available Tools:
{tools_list}

Response Format (JSON):
{{
    "reasoning": "Your step-by-step thinking",
    "action": "use_tool" or "final_answer",
    "tool_name": "tool name if using tool",
    "tool_input": "input for tool if using tool", 
    "response": "your final answer if done"
}}"""

def reason_agent(llm, state):
    """Perform reasoning and decide next action."""
    system_prompt = get_system_prompt()
    
    messages = [
        {"role": "system", "content": system_prompt},
        *state["messages"]
    ]
    
    response = llm.invoke(messages)
    
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {
            "reasoning": "LLM returned non-JSON response",
            "action": "final_answer",
            "response": response.content
        }