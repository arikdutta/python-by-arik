import streamlit as st
import os
import pypdf
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from typing import TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=api_key
)

MAX_CHARS = 15_000

CLASSIFY_SYSTEM = "You are a document classification expert. Respond with only the document type label — nothing else."

CLASSIFY_PROMPT = """Read the following document excerpt and classify it into exactly one of these categories:

- Resume / CV
- Medical Report
- Legal Contract
- Financial Statement
- Invoice / Receipt
- Academic Paper / Research
- Business Letter / Email
- Technical Documentation
- Government / Official Document
- News / Article
- Other

Respond with only the category name, exactly as written above.

Document:
{text}
"""

ANALYSIS_SYSTEM = "You are an expert document analyst. Provide clear, structured, and insightful analysis."

ANALYSIS_PROMPT = """You are analysing a **{doc_type}**.

Provide a comprehensive analysis of this document covering:

1. **Document Overview** – Summarise the purpose and key subject matter of this document.
2. **Key Information** – Extract and list the most important facts, figures, names, dates, or terms present.
3. **Main Findings / Highlights** – What are the most significant points or conclusions in this document?
4. **Notable Details** – Any unusual, critical, or noteworthy items that stand out.
5. **Potential Concerns or Gaps** – Identify anything missing, ambiguous, risky, or worth following up on.
6. **Summary & Next Steps** – A brief overall summary and any recommended actions based on the document content.

Document:
{text}
"""

# ── LangGraph candidate evaluation ──────────────────────────────────────────

class CandidateState(TypedDict):
    experience: int
    expected_salary: int
    fit_status: str
    rejection_level: str
    result: str


def salary_check(state: CandidateState):
    benchmark = (state["experience"] * 10000) + 10000
    overage = state["expected_salary"] - benchmark
    if overage <= 0:
        return {"fit_status": "Fit", "rejection_level": "None"}
    pct = overage / benchmark
    if pct <= 0.20:
        level = "Low"
    elif pct <= 0.50:
        level = "Medium"
    else:
        level = "High"
    return {"fit_status": "Unfit", "rejection_level": level}


def interview_questions(state: CandidateState):
    prompt = (
        f"Generate 5 concise technical interview questions for a candidate with "
        f"{state['experience']} year(s) of experience. Format as a numbered list."
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"result": response.content}


def rejection_summary(state: CandidateState):
    benchmark = (state["experience"] * 10000) + 10000
    overage = state["expected_salary"] - benchmark
    pct = round((overage / benchmark) * 100, 1)
    msg = (
        f"Candidate rejected. Expected salary ${state['expected_salary']:,} exceeds "
        f"the benchmark of ${benchmark:,} by ${overage:,} ({pct}%). "
        f"Rejection level: **{state['rejection_level']}**."
    )
    return {"result": msg}


def route_candidate(state: CandidateState):
    return "interview_node" if state["fit_status"] == "Fit" else "reject_node"


_candidate_graph = StateGraph(CandidateState)
_candidate_graph.add_node("salary_node", salary_check)
_candidate_graph.add_node("interview_node", interview_questions)
_candidate_graph.add_node("reject_node", rejection_summary)

_candidate_graph.set_entry_point("salary_node")
_candidate_graph.add_conditional_edges("salary_node", route_candidate)
_candidate_graph.add_edge("interview_node", END)
_candidate_graph.add_edge("reject_node", END)

candidate_app = _candidate_graph.compile()


def evaluate_candidate(experience: int, expected_salary: int) -> dict:
    return candidate_app.invoke({
        "experience": experience,
        "expected_salary": expected_salary,
        "fit_status": "",
        "rejection_level": "",
        "result": "",
    })


DOCUMENT_TYPE_ICONS = {
    "Resume / CV": "📄",
    "Medical Report": "🏥",
    "Legal Contract": "⚖️",
    "Financial Statement": "💰",
    "Invoice / Receipt": "🧾",
    "Academic Paper / Research": "🎓",
    "Business Letter / Email": "✉️",
    "Technical Documentation": "🔧",
    "Government / Official Document": "🏛️",
    "News / Article": "📰",
    "Other": "📁",
}


def extract_text_from_pdf(uploaded_file):
    reader = pypdf.PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_text_from_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8", errors="replace")


def extract_document_text(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif name.endswith(".txt"):
        text = extract_text_from_txt(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or TXT file.")
        return None

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]
        st.info("Document was truncated to fit the model's context window.")
    return text


def classify_document(text):
    prompt = CLASSIFY_PROMPT.format(text=text[:3000])
    messages = [
        SystemMessage(content=CLASSIFY_SYSTEM),
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(messages)
    label = response.content.strip()
    if label not in DOCUMENT_TYPE_ICONS:
        label = "Other"
    return label


def analyse_document(text, doc_type):
    prompt = ANALYSIS_PROMPT.format(doc_type=doc_type, text=text)
    messages = [
        SystemMessage(content=ANALYSIS_SYSTEM),
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(messages)
    return response.content


# ── UI ──────────────────────────────────────────────────────────────────────

st.title("AI Document Analyser")
st.caption("Upload any document — the AI will classify it and provide a structured analysis.")

uploaded_file = st.file_uploader(
    "Upload a document (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True,
)


if uploaded_file:
    docs_cache = st.session_state.setdefault("docs_cache", {})

    for file in uploaded_file:
        if file.name not in docs_cache:
            with st.spinner(f"Reading {file.name}..."):
                text = extract_document_text(file)
            if text is None:
                continue
            with st.spinner(f"Classifying {file.name}..."):
                doc_type = classify_document(text)
            docs_cache[file.name] = {"text": text, "doc_type": doc_type, "analysis": None}

    # Group uploaded files by document type (preserve upload order within each group)
    type_to_files: dict[str, list[str]] = {}
    for file in uploaded_file:
        if file.name not in docs_cache:
            continue
        doc_type = docs_cache[file.name]["doc_type"]
        type_to_files.setdefault(doc_type, []).append(file.name)

    if type_to_files:
        doc_types = list(type_to_files.keys())
        tab_labels = [
            f"{DOCUMENT_TYPE_ICONS.get(dt, '📁')} {dt}"
            + (f" ({len(type_to_files[dt])})" if len(type_to_files[dt]) > 1 else "")
            for dt in doc_types
        ]
        tabs = st.tabs(tab_labels)

        for tab, doc_type in zip(tabs, doc_types):
            with tab:
                for fname in type_to_files[doc_type]:
                    cached = docs_cache[fname]
                    icon = DOCUMENT_TYPE_ICONS.get(doc_type, "📁")

                    st.subheader(f"{icon} {fname}")
                    st.caption(f"Identified as a **{doc_type}**. Analysis is tailored to this document type.")

                    if st.button("Analyse Document", key=f"btn_{fname}", type="primary", use_container_width=True):
                        with st.spinner("Analysing..."):
                            try:
                                result = analyse_document(cached["text"], doc_type)
                                docs_cache[fname]["analysis"] = result
                            except Exception as e:
                                st.error(str(e))

                    if cached.get("analysis"):
                        st.markdown(cached["analysis"])

                    st.markdown("---")
    # ── Candidate evaluation panel (shown when any Resume/CV is present) ──────
    resume_files = [
        fname for fname, cached in docs_cache.items()
        if cached["doc_type"] == "Resume / CV"
    ]
    if resume_files:
        st.divider()
        st.subheader("🤖 Candidate Evaluation (LangGraph)")
        st.caption(
            "Enter the candidate's details to run the automated fit-check pipeline. "
            "The graph routes to interview questions or a rejection summary based on salary."
        )

        with st.form("candidate_form"):
            col1, col2 = st.columns(2)
            experience = col1.number_input("Years of experience", min_value=0, max_value=50, value=2, step=1)
            expected_salary = col2.number_input("Expected annual salary ($)", min_value=0, value=30000, step=1000)
            submitted = st.form_submit_button("Evaluate Candidate", type="primary", use_container_width=True)

        if submitted:
            benchmark = (experience * 10000) + 10000
            st.info(f"Salary benchmark for {experience} yr(s) experience: **${benchmark:,}**")
            with st.spinner("Running LangGraph evaluation..."):
                eval_result = evaluate_candidate(experience, expected_salary)

            fit = eval_result["fit_status"]
            if fit == "Fit":
                st.success("Result: **Fit** — Proceeding to interview stage")
                st.markdown("#### Interview Questions")
                st.markdown(eval_result["result"])
            else:
                level = eval_result["rejection_level"]
                colour = {"Low": "orange", "Medium": "red", "High": "darkred"}.get(level, "red")
                st.error(f"Result: **Unfit** — Rejection level: :{colour}[{level}]")
                st.markdown(eval_result["result"])

else:
    st.info("Upload one or more PDF or TXT files to get started.")
