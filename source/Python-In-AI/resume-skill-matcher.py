import anthropic
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

RESUMES_DIR = os.path.join(os.path.dirname(__file__), "sample-resumes")

SYSTEM_PROMPT = (
    "You are an expert HR recruiter. You will be given multiple resumes and a skill. "
    "Identify which candidate(s) best match that skill, explain why, and rank them if multiple qualify. "
    "Be concise and structured."
)


def load_file(path):
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
        print(f"  Error reading {path}: {e}")
        return None


def load_all_resumes(directory):
    resumes = {}
    if not os.path.isdir(directory):
        print(f"Resume directory not found: {directory}")
        return resumes
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        text = load_file(filepath)
        if text:
            resumes[filename] = text
    return resumes



def build_resume_context(resumes):
    parts = ["Here are the resumes you will use to answer skill-matching questions:\n"]
    for i, (name, text) in enumerate(resumes.items(), 1):
        parts.append(f"--- Resume {i}: {name} ---\n{text.strip()}\n")
    parts.append(
        "\nNow ask the user which skill they want to find the best match for."
    )
    return "\n".join(parts)


def run_chat(resumes):
    messages = [{"role": "user", "content": build_resume_context(resumes)}]

    while True:
        with client.messages.stream(
            model="claude-opus-4-8",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            print("\nAssistant: ", end="", flush=True)
            response_text = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                response_text += text
            print("\n")

        messages.append({"role": "assistant", "content": response_text})

        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})


def main():
    print("Resume Skill Matcher")
    print(f"Loading resumes from: {RESUMES_DIR}\n")

    resumes = load_all_resumes(RESUMES_DIR)
    if not resumes:
        print("No resumes found. Add files to the sample-resumes folder and retry.")
        return

    print(f"Loaded {len(resumes)} resume(s): {', '.join(resumes.keys())}\n")
    print("Starting chat... (type 'exit' or 'quit' to stop)\n")
    run_chat(resumes)


if __name__ == "__main__":
    main()
