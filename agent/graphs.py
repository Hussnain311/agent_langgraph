from langgraph.graph import StateGraph, END
from agents import reason_agent
from tools import get_tool
from models import AgentState
import json

def create_agent_graph(llm):
    """Create and compile the agent graph."""
    graph = StateGraph(AgentState)
    
    # Add nodes as functions
    graph.add_node("agent", lambda state: agent_node(llm, state))
    graph.add_node("tools", tools_node)
    graph.add_node("final", final_node)
    
    # Set entry point
    graph.set_entry_point("agent")
    
    # Define flow
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "final": "final"
        }
    )
    graph.add_edge("tools", "agent")
    graph.add_edge("final", END)
    
    return graph.compile()

def agent_node(llm, state):
    """Agent node - decides what to do next."""
    print(f"\n🤔 Step {state['step_count']}: Agent reasoning...")
    
    decision = reason_agent(llm, state)
    
    # Update state
    state["reasoning"].append(decision.get("reasoning", ""))
    state["current_step"] = decision.get("action", "final_answer")
    state["messages"].append({"role": "assistant", "content": json.dumps(decision)})
    
    print(f"   Reasoning: {decision.get('reasoning', '')}")
    print(f"   Decision: {decision.get('action')}")
    
    return state

def tools_node(state):
    """Tools node - executes the chosen tool."""
    last_message = state["messages"][-1]["content"]
    
    try:
        decision = json.loads(last_message)
        tool_name = decision.get("tool_name")
        tool_input = decision.get("tool_input")
        
        if tool_name and tool_input:
            tool_func = get_tool(tool_name)
            if tool_func:
                print(f"🛠️  Using {tool_name} with: '{tool_input}'")
                result = tool_func(tool_input)
                print(f"   Result: {result}")
                
                # Update state
                state["context"].append(result)
                state["tools_used"].append(tool_name)
                state["messages"].append({"role": "user", "content": f"Tool result: {result}"})
            else:
                state["error"] = f"Unknown tool: {tool_name}"
        else:
            state["error"] = "Missing tool name or input"
            
    except Exception as e:
        state["error"] = f"Tool execution error: {str(e)}"
    
    return state

def final_node(state):
    """Final node - prepares and displays the answer."""
    last_message = state["messages"][-1]["content"]
    
    try:
        decision = json.loads(last_message)
        final_answer = decision.get("response", "No answer provided")
    except:
        final_answer = last_message
    
    print(f"\n🎯 FINAL ANSWER:")
    print(f"   {final_answer}")
    print(f"\n📊 Summary: Used {len(state['tools_used'])} tools in {state['step_count']} steps")
    
    return state

def should_continue(state):
    """Decide where to go next."""
    if state.get("error"):
        return "final"
    
    current_step = state.get("current_step", "final")
    
    # Map agent decisions to graph nodes
    if current_step == "use_tool":
        return "tools"
    elif current_step == "final_answer":
        return "final"
    else:
        return "final"  # Default to final for unknown steps