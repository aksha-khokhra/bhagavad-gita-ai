from src.retriever.retriever import Retriever
from src.chatbot.prompt_builder import PromptBuilder
from src.chatbot.llm import LLMClient


OUT_OF_SCOPE_RESPONSE = (
    "I don't have enough information in the Bhagavad Gita "
    "knowledge base to answer that."
)


class Chatbot:
    def __init__(self):
        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()
        self.llm_client = LLMClient()

    def chat(self, user_query):
        retrieved_documents = self.retriever.retrieve(user_query)

        if retrieved_documents.get("route", {}).get("mode") == "out_of_scope":
            return OUT_OF_SCOPE_RESPONSE

        prompt = self.prompt_builder.build_prompt(
            user_query,
            retrieved_documents
        )

        response = self.llm_client.generate_response(prompt)

        return response
