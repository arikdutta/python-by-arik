import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[
        {
            "role": "user",
            "content": "What is Python?"
        }
    ]
)

for block in response.content:
    if block.type == "text":
        print(block.text)
