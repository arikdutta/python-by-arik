import streamlit as st
import anthropic
import os
import pypdf
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = "You are an expert HR recruiter and resume analyst. Keep responses clear, structured, and actionable."

MAX_RESUME_CHARS = 15_000

ANALYSIS_PROMPT = "Please analyze this resume thoroughly covering skills, experience, strengths, weaknesses, and give a hire recommendation.\n\nResume:\n"

SCORE_PROMPT = """Score this resume on a scale of 0-100 across these dimensions:

1. **Content & Relevance** (0-20) – Quality and relevance of experience, projects, and achievements.
2. **Skills Presentation** (0-20) – How well technical and soft skills are showcased.
3. **Formatting & Clarity** (0-20) – Structure, readability, and professional presentation.
4. **Impact & Quantification** (0-20) – Use of metrics, numbers, and measurable outcomes.
5. **ATS Compatibility** (0-20) – Keyword optimization and machine-readability.

For each dimension: give the score, a one-line reason, and one specific fix.
End with: **Overall Score: X/100** and a single sentence verdict.

Resume:
"""

SKILL_GAP_TEMPLATE = """Perform a skill gap analysis by comparing this resume against the job description below.

**Resume:**
{resume}

**Job Description:**
{job_desc}

Provide:
1. **Matched Skills** – Skills from the JD that the candidate already has.
2. **Missing Critical Skills** – Must-have skills from the JD that are absent.
3. **Missing Nice-to-Have Skills** – Preferred skills that are absent.
4. **Gap Severity** – Rate the overall gap: Low / Medium / High, with a one-line reason.
5. **Action Plan** – 3 concrete steps to close the most important gaps (courses, projects, certifications).
"""

IMPROVEMENT_PROMPT = """Review this resume and provide targeted improvement suggestions:

1. **Top 3 Weaknesses** – The most critical issues hurting this resume right now.
2. **Bullet Point Rewrites** – Pick 2-3 weak bullet points and rewrite them using STAR format with stronger action verbs and metrics.
3. **Missing Sections** – Identify any sections that should be added (e.g., summary, certifications, projects).
4. **Keywords to Add** – 5-8 high-value keywords missing that recruiters search for.
5. **Quick Wins** – 3 changes that take under 10 minutes but will immediately improve the resume.

Resume:
"""


def call_api(prompt):
    try:
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except anthropic.APIStatusError as e:
        if e.status_code >= 500:
            raise RuntimeError("Anthropic API is temporarily unavailable. Please try again in a moment.") from e
        raise


def extract_resume(uploaded_file):
    reader = pypdf.PdfReader(uploaded_file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if len(text) > MAX_RESUME_CHARS:
        text = text[:MAX_RESUME_CHARS]
        st.info("Resume was truncated to fit the model's context window.")
    return text


# ── UI ──────────────────────────────────────────────────────────────────────

st.title("AI Resume Analyser")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    if "resume_text" not in st.session_state or st.session_state.get("uploaded_name") != uploaded_file.name:
        st.session_state.resume_text = extract_resume(uploaded_file)
        st.session_state.uploaded_name = uploaded_file.name
        st.success(f"Resume loaded: {uploaded_file.name}")

tab1, tab2, tab3, tab4 = st.tabs(["Resume Analysis", "Resume Scoring", "Skill Gap Detection", "Improvement Suggestions"])

# ── Tab 1: Resume Analysis ───────────────────────────────────────────────────
with tab1:
    st.subheader("Resume Analysis")
    st.caption("Thorough breakdown of skills, experience, strengths, weaknesses, and a hire recommendation.")
    if st.button("Analyze Resume", key="btn_analyze"):
        if not uploaded_file:
            st.warning("Please upload a resume first.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    result = call_api(ANALYSIS_PROMPT + st.session_state.resume_text)
                    st.markdown(result)
                except (RuntimeError, anthropic.APIError) as e:
                    st.error(str(e))

# ── Tab 2: Resume Scoring ────────────────────────────────────────────────────
with tab2:
    st.subheader("Resume Scoring")
    st.caption("Score your resume 0–100 across 5 dimensions with a specific fix for each.")
    if st.button("Score Resume", key="btn_score"):
        if not uploaded_file:
            st.warning("Please upload a resume first.")
        else:
            with st.spinner("Scoring..."):
                try:
                    result = call_api(SCORE_PROMPT + st.session_state.resume_text)
                    st.markdown(result)
                except (RuntimeError, anthropic.APIError) as e:
                    st.error(str(e))

# ── Tab 3: Skill Gap Detection ───────────────────────────────────────────────
with tab3:
    st.subheader("Skill Gap Detection")
    st.caption("Compare your resume against a job description to find matched and missing skills.")
    job_desc = st.text_area("Paste the job description here:", height=200, key="job_desc_input")
    if st.button("Detect Skill Gaps", key="btn_gap"):
        if not uploaded_file:
            st.warning("Please upload a resume first.")
        elif not job_desc.strip():
            st.warning("Please paste a job description.")
        else:
            with st.spinner("Analysing skill gaps..."):
                try:
                    prompt = SKILL_GAP_TEMPLATE.format(
                        resume=st.session_state.resume_text,
                        job_desc=job_desc,
                    )
                    result = call_api(prompt)
                    st.markdown(result)
                except (RuntimeError, anthropic.APIError) as e:
                    st.error(str(e))

# ── Tab 4: Improvement Suggestions ──────────────────────────────────────────
with tab4:
    st.subheader("Improvement Suggestions")
    st.caption("Get targeted fixes: rewritten bullet points, missing sections, keywords to add, and quick wins.")
    if st.button("Get Suggestions", key="btn_improve"):
        if not uploaded_file:
            st.warning("Please upload a resume first.")
        else:
            with st.spinner("Generating suggestions..."):
                try:
                    result = call_api(IMPROVEMENT_PROMPT + st.session_state.resume_text)
                    st.markdown(result)
                except (RuntimeError, anthropic.APIError) as e:
                    st.error(str(e))
