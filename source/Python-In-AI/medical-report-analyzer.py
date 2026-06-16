import anthropic
import os
import sys
import pypdf
from dotenv import load_dotenv

load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a board-certified physician and clinical laboratory specialist with 20+ years of experience interpreting diagnostic reports.

When given a medical report, analyze it and provide a structured clinical summary with:

1. **Patient Overview**: Name, age, sex, visit date, and reason for visit
2. **Overall Health Status**: One of — NORMAL / BORDERLINE / ABNORMAL — with a brief justification
3. **Vital Signs Assessment**: Interpretation of BP, HR, BMI, temperature, SpO2, and any other vitals present
4. **Lab Findings — Flagged Results**: List every out-of-range value with the result, reference range, and clinical significance
5. **Lab Findings — Normal Results**: Briefly confirm which panels are within range
6. **Identified Conditions / Risks**: List any confirmed conditions, borderline states, or elevated risk factors inferred from the data (e.g., pre-diabetes, dyslipidaemia, hypertension)
7. **Recommended Actions**: Specific next steps — lifestyle changes, follow-up tests, specialist referrals, or medication review
8. **Urgency Level**: One of — ROUTINE / MONITOR / URGENT — indicating how quickly the patient should follow up

Be precise, clinically grounded, and actionable. Use plain language where possible so the report is understandable to both clinicians and informed patients. Format your response clearly with section headers.

IMPORTANT: Always note that this is an AI-assisted analysis and does not replace professional medical advice."""


def load_report_from_file(filepath):
    if filepath.lower().endswith(".pdf"):
        reader = pypdf.PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def analyze_report(report_text):
    user_message = f"Please analyze the following medical report:\n\n{report_text}"

    print("\nAnalyzing medical report...\n")
    print("-" * 60)

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n" + "-" * 60)


def select_report():
    reports_dir = "C:\\Users\\dutta\\python-by-arik\\SampleMedicalReports"
    try:
        files = [f for f in os.listdir(reports_dir) if f.lower().endswith(".pdf")]
    except FileNotFoundError:
        print(f"Reports directory not found: {reports_dir}")
        return None

    if not files:
        print("No PDF reports found in the directory.")
        return None

    print("\nAvailable medical reports:")
    for i, name in enumerate(files, 1):
        print(f"  {i}. {name}")

    print(f"  {len(files) + 1}. Enter a custom file path")
    print("\nSelect a report number:", end=" ")
    choice = input().strip()

    try:
        idx = int(choice)
        if 1 <= idx <= len(files):
            return os.path.join(reports_dir, files[idx - 1])
        elif idx == len(files) + 1:
            print("Enter full file path: ", end="")
            return input().strip().strip('"')
    except ValueError:
        pass

    print("Invalid selection.")
    return None


def main():
    print("=== Medical Report Analyzer ===")
    print("AI-assisted patient condition assessment\n")

    filepath = select_report()
    if not filepath or not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    report_text = load_report_from_file(filepath)
    print(f"\nLoaded report from: {os.path.basename(filepath)}")

    analyze_report(report_text)

    while True:
        print("\nOptions:")
        print("1. Analyze another report")
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
