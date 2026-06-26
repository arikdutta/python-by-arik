import streamlit as st
import os
import pypdf
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import json

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=api_key,
)

MAX_CHARS = 15_000

# ── Tools ────────────────────────────────────────────────────────────────────

@tool
def estimate_ctc(
    years_of_experience: int,
    role: str,
    skills: list[str],
    education_level: str,
    location: str,
    current_ctc_lpa: float,
) -> dict:
    """Estimate CTC range in LPA (Lakhs Per Annum) for an Indian software professional
    based on their profile extracted from a resume.

    Args:
        years_of_experience: Total years of professional experience.
        role: Current or target job role (e.g. 'Software Engineer', 'Data Scientist').
        skills: List of key technical skills (e.g. ['Python', 'React', 'AWS']).
        education_level: Highest education level (e.g. 'B.Tech', 'M.Tech', 'MBA', 'PhD').
        location: City or region (e.g. 'Bangalore', 'Mumbai', 'Hyderabad').
        current_ctc_lpa: Current CTC in LPA; 0 if fresher or unknown.
    """
    # Base salary by experience band (LPA)
    if years_of_experience == 0:
        base_min, base_max = 4.0, 8.0
    elif years_of_experience <= 2:
        base_min, base_max = 6.0, 14.0
    elif years_of_experience <= 5:
        base_min, base_max = 12.0, 25.0
    elif years_of_experience <= 8:
        base_min, base_max = 22.0, 40.0
    elif years_of_experience <= 12:
        base_min, base_max = 35.0, 60.0
    else:
        base_min, base_max = 55.0, 100.0

    # Role multiplier (senior/lead/architect roles command higher pay)
    role_lower = role.lower()
    if any(k in role_lower for k in ("principal", "architect", "vp", "director", "head")):
        role_mult = 1.25
    elif any(k in role_lower for k in ("senior", "lead", "staff", "manager")):
        role_mult = 1.10
    elif any(k in role_lower for k in ("junior", "intern", "trainee", "fresher")):
        role_mult = 0.90
    else:
        role_mult = 1.0

    # Education multiplier
    edu_multiplier = {
        "phd": 1.20,
        "m.tech": 1.15,
        "mtech": 1.15,
        "mba": 1.15,
        "m.sc": 1.10,
        "msc": 1.10,
        "b.tech": 1.0,
        "btech": 1.0,
        "b.e": 1.0,
        "be": 1.0,
        "bsc": 0.95,
        "b.sc": 0.95,
    }
    edu_key = education_level.lower().strip()
    multiplier = next((v for k, v in edu_multiplier.items() if k in edu_key), 1.0)

    # Premium skills bonus (LPA)
    premium_skills = {
        "machine learning", "deep learning", "llm", "genai", "generative ai",
        "kubernetes", "aws", "azure", "gcp", "devops", "golang", "rust",
        "blockchain", "react native", "flutter", "spark", "kafka",
    }
    skill_set = {s.lower() for s in skills}
    premium_count = len(skill_set & premium_skills)
    skill_bonus = min(premium_count * 1.5, 8.0)

    # Location multiplier
    tier1 = {"bangalore", "bengaluru", "mumbai", "delhi", "hyderabad", "pune", "chennai", "gurgaon", "noida"}
    loc_mult = 1.10 if location.lower() in tier1 else 1.0

    estimated_min = round((base_min * multiplier + skill_bonus) * loc_mult * role_mult, 1)
    estimated_max = round((base_max * multiplier + skill_bonus) * loc_mult * role_mult, 1)

    # If current CTC is known, floor estimate at 20% hike
    if current_ctc_lpa > 0:
        hike_floor = round(current_ctc_lpa * 1.20, 1)
        estimated_min = max(estimated_min, hike_floor)
        estimated_max = max(estimated_max, round(current_ctc_lpa * 1.40, 1))

    return {
        "estimated_ctc_range_lpa": f"{estimated_min} – {estimated_max}",
        "min_lpa": estimated_min,
        "max_lpa": estimated_max,
        "rationale": {
            "experience_band": f"{years_of_experience} yrs → base {base_min}–{base_max} LPA",
            "role_multiplier": f"{role_mult}x for {role}",
            "education_multiplier": f"{multiplier}x for {education_level}",
            "premium_skill_bonus": f"+{skill_bonus} LPA ({premium_count} premium skills found)",
            "location_multiplier": f"{loc_mult}x for {location}",
        },
    }


@tool
def build_ctc_breakdown(total_ctc_lpa: float) -> dict:
    """Break down total CTC (in LPA) into standard Indian salary components.

    Args:
        total_ctc_lpa: Total annual CTC in Lakhs Per Annum.
    """
    annual = total_ctc_lpa * 100_000  # convert to rupees

    basic = round(annual * 0.40)
    hra = round(annual * 0.20)
    pf_employee = round(basic * 0.12)
    pf_employer = round(basic * 0.12)
    special_allowance = round(annual * 0.20 - pf_employer)
    performance_bonus = round(annual * 0.10)
    gratuity = round(basic * 4.81 / 100)
    esic = round(annual * 0.0075) if annual <= 2_100_000 else 0

    gross_monthly = round((basic + hra + special_allowance + performance_bonus / 12) / 12)
    in_hand_monthly = round(gross_monthly - pf_employee / 12)

    def fmt(amount):
        return f"₹{amount:,.0f}"

    return {
        "annual_breakdown": {
            "Basic Salary (40%)": fmt(basic),
            "HRA (20%)": fmt(hra),
            "Special Allowance (~20%)": fmt(special_allowance),
            "Performance Bonus (~10%)": fmt(performance_bonus),
            "PF – Employee (12% of Basic)": fmt(pf_employee),
            "PF – Employer (12% of Basic)": fmt(pf_employer),
            "Gratuity": fmt(gratuity),
            "ESIC (if applicable)": fmt(esic),
        },
        "monthly_estimates": {
            "Gross Monthly": fmt(gross_monthly),
            "Approx. In-Hand Monthly": fmt(in_hand_monthly),
        },
        "total_ctc": fmt(int(annual)),
    }


TOOLS = [estimate_ctc, build_ctc_breakdown]
llm_with_tools = llm.bind_tools(TOOLS)
tool_map = {t.name: t for t in TOOLS}

# ── Prompts ───────────────────────────────────────────────────────────────────

EXTRACT_SYSTEM = """You are an expert HR analyst. Given a resume, you will:
1. Call the estimate_ctc tool with details extracted from the resume.
2. Then call the build_ctc_breakdown tool using the midpoint of the estimated range.
3. Provide a concise salary assessment narrative (3-4 sentences) that justifies the estimate.

Always call both tools. Extract the best values you can from the resume."""

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_text_from_pdf(uploaded_file) -> str:
    reader = pypdf.PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_text(uploaded_file) -> str | None:
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8", errors="replace")
    else:
        st.error("Unsupported file type. Please upload a PDF or TXT file.")
        return None
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]
        st.info("Resume was truncated to fit the model's context window.")
    return text


def run_salary_agent(resume_text: str) -> dict:
    """Run the two-step tool-calling agent and return structured results."""
    messages = [
        SystemMessage(content=EXTRACT_SYSTEM),
        HumanMessage(content=f"Here is the candidate's resume:\n\n{resume_text}"),
    ]

    ctc_result = None
    breakdown_result = None
    narrative = ""

    for _ in range(6):  # safety cap on iterations
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            narrative = response.content
            break

        for tc in response.tool_calls:
            tool_fn = tool_map.get(tc["name"])
            if tool_fn is None:
                continue
            result = tool_fn.invoke(tc["args"])
            if tc["name"] == "estimate_ctc":
                ctc_result = result
            elif tc["name"] == "build_ctc_breakdown":
                breakdown_result = result
            messages.append(
                ToolMessage(content=json.dumps(result), tool_call_id=tc["id"])
            )

    return {
        "ctc_estimate": ctc_result,
        "ctc_breakdown": breakdown_result,
        "narrative": narrative,
    }


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("AI CTC Calculator")
st.caption("Upload a resume — the AI extracts your profile and estimates your market salary using LangChain tools.")

uploaded_file = st.file_uploader("Upload resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    cache = st.session_state.setdefault("ctc_cache", {})

    if uploaded_file.name not in cache:
        with st.spinner("Reading resume..."):
            text = extract_text(uploaded_file)
        if text:
            cache[uploaded_file.name] = {"text": text, "result": None}
        else:
            st.stop()

    cached = cache[uploaded_file.name]

    if st.button("Calculate Salary", type="primary", use_container_width=True):
        with st.spinner("Analysing resume and estimating CTC..."):
            try:
                cached["result"] = run_salary_agent(cached["text"])
            except Exception as e:
                st.error(f"Error: {e}")

    result = cached.get("result")
    if result:
        ctc = result.get("ctc_estimate") or {}
        breakdown = result.get("ctc_breakdown") or {}
        narrative = result.get("narrative", "")

        # Header metric
        if ctc.get("estimated_ctc_range_lpa"):
            st.markdown("---")
            col1, col2 = st.columns(2)
            col1.metric("Estimated CTC Range", f"{ctc['estimated_ctc_range_lpa']} LPA")
            if breakdown.get("monthly_estimates"):
                in_hand = breakdown["monthly_estimates"].get("Approx. In-Hand Monthly", "—")
                col2.metric("Approx. In-Hand (Monthly)", in_hand)

        # Rationale
        if ctc.get("rationale"):
            with st.expander("How was this calculated?", expanded=False):
                for k, v in ctc["rationale"].items():
                    st.write(f"**{k.replace('_', ' ').title()}:** {v}")

        # Annual breakdown
        if breakdown.get("annual_breakdown"):
            st.subheader("Annual CTC Breakdown")
            rows = [{"Component": k, "Amount": v} for k, v in breakdown["annual_breakdown"].items()]
            st.table(rows)

        # Monthly summary
        if breakdown.get("monthly_estimates"):
            st.subheader("Monthly Estimates")
            cols = st.columns(len(breakdown["monthly_estimates"]))
            for col, (label, value) in zip(cols, breakdown["monthly_estimates"].items()):
                col.metric(label, value)

        # Narrative
        if narrative:
            st.markdown("---")
            st.subheader("Analyst Assessment")
            st.markdown(narrative)

else:
    st.info("Upload a PDF or TXT resume to get started.")
