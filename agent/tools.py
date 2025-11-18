import ast
import operator as op
from langchain_community.tools import DuckDuckGoSearchRun

# Calculator as simple function
def calculate_expression(expression: str) -> str:
    """Safe calculator using AST parsing."""
    allowed_operators = {
        ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, 
        ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod,
        ast.USub: op.neg
    }
    
    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = eval_expr(node.left)
            right = eval_expr(node.right)
            return allowed_operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = eval_expr(node.operand)
            return allowed_operators[type(node.op)](operand)
        else:
            raise TypeError(f"Unsupported operation: {type(node)}")
    
    try:
        tree = ast.parse(expression, mode='eval')
        result = eval_expr(tree.body)
        return f"The result of '{expression}' is {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"

# Search as simple function
def search_web(query: str) -> str:
    """Web search using DuckDuckGo."""
    try:
        search = DuckDuckGoSearchRun()
        result = search.run(query)
        return f"Search results for '{query}':\n{result}"
    except Exception as e:
        return f"Error searching for '{query}': {str(e)}"

# Tool registry as functions
def get_tool(tool_name: str):
    """Get tool function by name."""
    tools = {
        "calculator": calculate_expression,
        "web_search": search_web
    }
    return tools.get(tool_name)

def list_tools():
    """List all available tools."""
    return ["calculator", "web_search"]