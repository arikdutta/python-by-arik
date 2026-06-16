import os
import anthropic
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class ResumeInput(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    summary: str
    experience: str
    education: str
    skills: str
    certifications: str = ""


@router.post("/build")
async def build_resume(data: ResumeInput):
    prompt = f"""You are an expert resume writer. Create a polished, professional resume in clean Markdown format based on the following information:

Name: {data.name}
Email: {data.email}
Phone: {data.phone}
Location: {data.location}

Professional Summary:
{data.summary}

Work Experience:
{data.experience}

Education:
{data.education}

Skills:
{data.skills}

Certifications:
{data.certifications}

Instructions:
- Format it as a complete, ATS-friendly resume in Markdown
- Enhance the language to be impactful and results-oriented
- Add strong action verbs and quantifiable achievements where possible
- Organize sections clearly: Contact Info, Summary, Experience, Education, Skills, Certifications
- Make it concise and recruiter-friendly"""

    def generate():
        with client.messages.stream(
            model="claude-opus-4-8",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/plain")
