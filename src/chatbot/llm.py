import ollama

from src.knowledge_base.config import OLLAMA_MODEL

class LLMClient:
    
    def __init__(self):
        self.model = OLLAMA_MODEL

    def generate_response(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        return response["message"]["content"]