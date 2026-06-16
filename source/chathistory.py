import anthropic
import os
import pypdf
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant and expert HR recruiter.
When resumes are loaded, evaluate candidates for backend engineering roles based on:
- Backend languages (Python, Java, Go, Node.js, etc.)
- Databases (SQL, NoSQL, caching)
- APIs and system design experience
- Cloud/DevOps familiarity
Provide clear ELIGIBLE / NOT ELIGIBLE verdicts with reasoning when asked."""


def load_resumes(folder_path):
    resumes = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            reader = pypdf.PdfReader(filepath)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            resumes[filename] = text
    return resumes


print("Chat started. Type 'load <folder_path>' to load resumes, or 'exit' to quit.\n")

messages = []

while True:
    user = input("You: ").strip()

    if user.lower() in ("exit", "quit"):
        break

    if user.lower().startswith("load "):
        folder_path = user[5:].strip().strip('"').strip("'")
        if not os.path.isdir(folder_path):
            print(f"Folder not found: {folder_path}\n")
            continue

        resumes = load_resumes(folder_path)
        if not resumes:
            print("No PDF resumes found in that folder.\n")
            continue

        print(f"\nLoaded {len(resumes)} resume(s):")
        for i, name in enumerate(resumes.keys(), 1):
            print(f"  {i}. {name}")
        print()

        resume_context = "\n\n".join(
            f"=== Resume: {name} ===\n{text}" for name, text in resumes.items()
        )
        messages.append({"role": "user", "content": f"Here are the candidate resumes:\n\n{resume_context}"})
        messages.append({"role": "assistant", "content": f"I've reviewed all {len(resumes)} resume(s). Ask me anything about the candidates."})
        print(f"Assistant: I've reviewed all {len(resumes)} resume(s). Ask me anything about the candidates.\n")
        continue

    messages.append({"role": "user", "content": user})

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        thinking={"type": "adaptive"},
        messages=messages
    )

    answer = next(block.text for block in response.content if block.type == "text")

    messages.append({"role": "assistant", "content": response.content})

    print(f"\nAssistant: {answer}\n")
