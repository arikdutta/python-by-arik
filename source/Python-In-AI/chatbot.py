import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

conversation_history = []

SYSTEM_PROMPT = "You are a helpful and friendly AI assistant. Be concise but informative in your responses."

print("Chatbot ready! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    conversation_history.append({"role": "user", "content": user_input})

    print("Bot: ", end="", flush=True)

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation_history,
    ) as stream:
        full_response = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print()

    conversation_history.append({"role": "assistant", "content": full_response})
