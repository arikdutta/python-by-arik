import os
import anthropic
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class JobDescriptionInput(BaseModel):
    job_title: str
    company_name: str
    department: str = ""
    employment_type: str = "Full-time"
    location: str = ""
    responsibilities: str
    requirements: str
    nice_to_have: str = ""
    salary_range: str = ""
    about_company: str = ""


@router.post("/create")
async def create_job_description(data: JobDescriptionInput):
    prompt = f"""You are an expert HR professional and technical recruiter. Create a compelling, detailed job description in Markdown format based on the following details:

Job Title: {data.job_title}
Company: {data.company_name}
Department: {data.department}
Employment Type: {data.employment_type}
Location: {data.location}
Salary Range: {data.salary_range}

About the Company:
{data.about_company}

Key Responsibilities:
{data.responsibilities}

Required Qualifications:
{data.requirements}

Nice to Have:
{data.nice_to_have}

Instructions:
- Write an engaging, professional job description in Markdown
- Include sections: Job Overview, About the Role, Key Responsibilities, Requirements, Nice to Have, What We Offer
- Use bullet points for clarity
- Make it attractive to top talent while being realistic
- Include inclusive language
- Highlight growth opportunities and company culture"""

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
