import asyncio
from config import Config
from graphs import create_agent_graph
from models import AgentState

async def main():
    """Main function with example queries."""
    llm = Config.get_llm()
    app = create_agent_graph(llm)
    
    query = input("ENter Your Question :")
    
    print(f"\n{'='*60}")
    print(f"🧠 QUESTION: {query}")
    print(f"{'='*60}")
        
        # Initialize state
    state = AgentState(
        input=query,
        messages=[{"role": "user", "content": query}],
        context=[],
        reasoning=[],
        current_step="start",
        step_count=0,
        tools_used=[],
        error=None
    )
        
      
    final_state = app.invoke(state)
        
        # Print reasoning
    print(f"\n🔍 REASONING CHAIN:")
    for i, reasoning in enumerate(final_state["reasoning"]):
        if reasoning:
                print(f"   {i+1}. {reasoning}")
        
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(main())