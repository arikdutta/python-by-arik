import anthropic
import os
import pypdf
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
 
def load_resume_from_file(filepath):
    if filepath.lower().endswith(".pdf"):
        reader = pypdf.PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
    
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
    
filepath = prompt_for_resume()
resume_text = load_resume_from_file(filepath)

 
response = client.messages.create(
 
        model="claude-opus-4-8",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        messages=[
            {
                "role":"user",
                "content":f"""
 
Analyze this resume.
 
Give:
 
1. Strengths
 
2. Weaknesses
 
3. Missing Skills
 
4. Improvement Suggestions
 
Resume:
 
{resume_text}
 
"""
            }
        ]
    )
 
for block in response.content:
    if block.type == "text":
        print(block.text)