import anthropic
import os
import pypdf
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert HR recruiter and talent acquisition specialist with 15+ years of experience screening candidates.

When given a resume, analyze it and provide a structured screening report with:

1. **Overall Score** (1-10): A numeric rating of the candidate's overall fit
2. **Key Skills**: List of relevant technical and soft skills detected
3. **Strengths**: Top 3-5 strongest points about the candidate
4. **Weaknesses / Gaps**: Areas of concern or missing qualifications
5. **Experience Summary**: Brief overview of their background
6. **Recommendation**: One of — STRONG HIRE / HIRE / CONSIDER / REJECT — with a one-line reason

If a job description is provided, tailor your analysis to how well the candidate matches that specific role.

Be concise, objective, and actionable. Format your response clearly with section headers."""


def load_resume_from_file(filepath):
    if filepath.lower().endswith(".pdf"):
        reader = pypdf.PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def analyze_resume(resume_text, job_description=None):
    user_message = f"Please analyze the following resume:\n\n{resume_text}"
    if job_description:
        user_message += f"\n\n---\nJob Description to match against:\n{job_description}"

    print("\nAnalyzing resume...\n")
    print("-" * 60)

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n" + "-" * 60)


def prompt_for_resume():
    while True:
        print("Enter the path to the resume PDF (or drag and drop the file here):")
        filepath = input("Resume path: ").strip().strip('"').strip("'")
        if not filepath:
            print("No path entered. Please try again.\n")
            continue
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}\nPlease check the path and try again.\n")
            continue
        if not filepath.lower().endswith((".pdf", ".txt")):
            print("Only .pdf and .txt files are supported. Please try again.\n")
            continue
        return filepath


def main():
    print("=== Resume Analyzer ===")
    print("Screen candidates using AI\n")

    filepath = prompt_for_resume()
    resume_text = load_resume_from_file(filepath)
    print(f"\nLoaded resume from: {filepath}")

    print("\nOptional: Enter a job description to match the candidate against.")
    print("Press Enter to skip, or type 'JD' to add one:")
    jd_choice = input().strip()

    job_description = None
    if jd_choice.upper() == "JD":
        print("\nPaste the job description. Enter a blank line followed by 'END' to finish:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        job_description = "\n".join(lines)

    analyze_resume(resume_text, job_description)

    while True:
        print("\nOptions:")
        print("1. Analyze another resume")
        print("2. Exit")
        option = input("Choice: ").strip()
        if option == "1":
            main()
            break
        else:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
