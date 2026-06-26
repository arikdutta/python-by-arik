from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("ANTHROPIC_API_KEY")

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=api_key
)

history = [SystemMessage(content="You are a helpful assistant.")]

print("Chatbot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit"):
        print("Goodbye!")
        break

    history.append(HumanMessage(content=user_input))

    response = llm.invoke(history)

    history.append(AIMessage(content=response.content))

    print(f"Assistant: {response.content}\n")
