import _bootstrap  # noqa: F401
from src.chatbot.chatbot import Chatbot

chatbot = Chatbot()

while True:
    user_query = input("You: ").strip()

    if user_query.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break

    response = chatbot.chat(user_query)
    
    print(f"\nProject Tattva: {response}\n")