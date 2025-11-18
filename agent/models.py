from typing import TypedDict, List, Annotated, Optional
import operator

class AgentState(TypedDict):
    """Main state for our agent workflow."""
    input: str
    messages: List[dict]
    context: List[str]
    reasoning: List[str]
    current_step: str
    step_count: Annotated[int, operator.add]
    tools_used: List[str]
    error: Optional[str]