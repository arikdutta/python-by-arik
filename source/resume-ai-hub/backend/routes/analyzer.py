import os
import anthropic
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class AnalyzerInput(BaseModel):
    resume: str
    job_description: str


@router.post("/analyze")
async def analyze_resume(data: AnalyzerInput):
    prompt = f"""You are an expert recruiter and career coach with 20 years of experience in talent acquisition.
Perform a comprehensive analysis of this resume against the job description.

RESUME:
{data.resume}

JOB DESCRIPTION:
{data.job_description}

Provide a detailed analysis in Markdown with these sections:

## Overall Match Score
Give a percentage match score (0-100%) with a brief explanation.

## Strengths
List the candidate's strengths that align well with the role (bullet points).

## Skill Gaps
List skills or experience mentioned in the JD that are missing or weak in the resume (bullet points).

## ATS Keywords Analysis
- Keywords found in both resume and JD
- Important JD keywords missing from resume

## Recommendations
Specific, actionable advice to improve the resume for this role (numbered list).

## Interview Prep Tips
3-5 likely interview questions based on the JD and resume gaps, with brief tips on how to answer each.

## Final Verdict
A concise recruiter-style assessment: would you shortlist this candidate? Why or why not?"""

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
