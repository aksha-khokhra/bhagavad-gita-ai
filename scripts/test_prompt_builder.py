import _bootstrap  # noqa: F401
from src.chatbot.prompt_builder import PromptBuilder
from src.retriever.retriever import Retriever

retriever = Retriever()

prompt_builder = PromptBuilder()

user_query = "Why should we perform actions without expecting results?"

retrieved_documents = retriever.retrieve(user_query)

prompt = prompt_builder.build_prompt(user_query, retrieved_documents)

print(prompt)