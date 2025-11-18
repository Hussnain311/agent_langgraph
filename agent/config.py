import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o"
    
    # Agent
    MAX_STEPS = 10
    TEMPERATURE = 0.1
    
    @classmethod
    def get_llm(cls):
        """Get configured LLM instance."""
        return ChatOpenAI(
            model=cls.OPENAI_MODEL,
            temperature=cls.TEMPERATURE,
            api_key=cls.OPENAI_API_KEY
        )