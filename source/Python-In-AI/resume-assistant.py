import anthropic
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

conversation_history = []
last_resume_text = None

SYSTEM_PROMPT = "You are an expert HR recruiter and resume analyst. When the user shares a resume, analyze it thoroughly covering skills, experience, strengths, weaknesses, and give a hire recommendation. Keep responses clear and structured."

CAREER_PATH_PROMPT = """Based on this resume, provide a detailed career path analysis:
1. **Ideal Roles Now** – 2-3 job titles that best match current skills and experience level.
2. **Short-Term Path (1-3 years)** – Skills to build, roles to target, and certifications to pursue.
3. **Long-Term Path (5-10 years)** – Senior/leadership roles this person could realistically reach.
4. **Alternative Paths** – 1-2 adjacent industries or pivot opportunities suited to their background.
5. **Key Gaps to Address** – What's holding them back from the next level.

Resume:
"""

print("Career Assistant ready! Type 'exit' to quit.")
print("Commands: 'load <path>' to load a resume file, 'file' to browse by path, 'paste' to paste text, 'path' to get career path recommendations.\n")


def load_resume_file(path):
    path = path.strip().strip('"').strip("'")
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".pdf":
            reader = PdfReader(path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        elif ext in (".docx", ".doc"):
            doc = Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        else:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def collect_pasted_resume():
    print("Paste your resume below. Press Enter twice when done:")
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        lines.append(line)
    return "\n".join(lines)


def send_message(content):
    conversation_history.append({"role": "user", "content": content})
    print("\nBot: ", end="", flush=True)
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
    print("\n")
    conversation_history.append({"role": "assistant", "content": full_response})


startup_path = input("Enter resume file path to analyze (or press Enter to skip): ").strip().strip('"').strip("'")
if startup_path:
    resume_text = load_resume_file(startup_path)
    if resume_text:
        last_resume_text = resume_text
        send_message(f"Please analyze this resume:\n\n{resume_text}")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    if user_input.lower().startswith("load "):
        path = user_input[5:]
        resume_text = load_resume_file(path)
        if resume_text:
            last_resume_text = resume_text
            send_message(f"Please analyze this resume:\n\n{resume_text}")
        continue

    if user_input.lower() == "file":
        file_path = input("Enter resume file path: ").strip().strip('"').strip("'")
        resume_text = load_resume_file(file_path)
        if resume_text:
            last_resume_text = resume_text
            send_message(f"Please analyze this resume:\n\n{resume_text}")
        continue

    if user_input.lower() == "paste":
        resume_text = collect_pasted_resume()
        if resume_text:
            last_resume_text = resume_text
            send_message(f"Please analyze this resume:\n\n{resume_text}")
        continue

    if user_input.lower() == "path":
        if not last_resume_text:
            print("No resume loaded yet. Use 'load <path>', 'file', or 'paste' first.\n")
        else:
            send_message(f"{CAREER_PATH_PROMPT}{last_resume_text}")
        continue

    send_message(user_input)
