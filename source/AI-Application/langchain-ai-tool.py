import streamlit as st
import os
import re
import pypdf
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("ANTHROPIC_API_KEY not set. Add it to your .env file.")
    st.stop()

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=api_key)

MAX_CHARS = 15_000

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


# ── Tools ─────────────────────────────────────────────────────────────────────
# Each tool is a small, focused capability that agents can call.

@tool
def extract_entities(text: str) -> str:
    """Extract named entities like dates, money amounts, emails, and percentages
    from a document. Use this to pull out concrete facts and figures."""
    dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b", text)
    money = re.findall(r"[$€£]\s?\d[\d,]*(?:\.\d+)?", text)
    emails = re.findall(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", text)
    percents = re.findall(r"\b\d+(?:\.\d+)?\s?%", text)
    return (
        f"Dates: {sorted(set(dates))[:20]}\n"
        f"Money: {sorted(set(money))[:20]}\n"
        f"Emails: {sorted(set(emails))[:20]}\n"
        f"Percentages: {sorted(set(percents))[:20]}"
    )


@tool
def document_stats(text: str) -> str:
    """Compute basic statistics about a document: word count, character count,
    and an estimated reading time. Use this for a quick quantitative overview."""
    words = len(text.split())
    chars = len(text)
    read_min = max(1, round(words / 200))
    return f"Words: {words}, Characters: {chars}, Est. reading time: {read_min} min"


TOOLS = [extract_entities, document_stats]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}


# ── Agents ────────────────────────────────────────────────────────────────────
# Three specialised agents, each with its own system prompt and role.

def run_agent(system_prompt: str, user_prompt: str, use_tools: bool = False) -> str:
    """Run a single agent turn. If use_tools is True, the agent may call tools
    and we feed the results back for a final answer."""
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

    if not use_tools:
        return llm.invoke(messages).content

    bound = llm.bind_tools(TOOLS)
    response = bound.invoke(messages)
    messages.append(response)

    # Execute any tool calls and feed results back
    if response.tool_calls:
        for call in response.tool_calls:
            tool_fn = TOOLS_BY_NAME[call["name"]]
            result = tool_fn.invoke(call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
        response = bound.invoke(messages)

    return response.content


def classifier_agent(text: str) -> str:
    """Agent 1: classifies the document type."""
    categories = "\n".join(f"- {k}" for k in DOCUMENT_TYPE_ICONS)
    label = run_agent(
        system_prompt="You are a document classification expert. Respond with only the document type label — nothing else.",
        user_prompt=f"Classify this document into exactly one category:\n{categories}\n\nDocument:\n{text[:3000]}",
    ).strip()
    return label if label in DOCUMENT_TYPE_ICONS else "Other"


def extractor_agent(text: str, doc_type: str) -> str:
    """Agent 2: uses tools to pull out structured facts."""
    return run_agent(
        system_prompt="You are a data extraction specialist. Use the available tools to gather "
        "facts about the document, then present them as a clean bulleted summary.",
        user_prompt=f"This is a {doc_type}. Extract key facts and stats from it.\n\nDocument:\n{text}",
        use_tools=True,
    )


def analyst_agent(text: str, doc_type: str, extraction: str) -> str:
    """Agent 3: writes the final narrative analysis, informed by the extractor's output."""
    return run_agent(
        system_prompt="You are an expert document analyst. Provide clear, structured, insightful analysis.",
        user_prompt=f"""You are analysing a **{doc_type}**.

A data-extraction agent already gathered these facts:
{extraction}

Now provide a comprehensive analysis covering:
1. **Document Overview** – purpose and subject matter.
2. **Key Information** – important facts, figures, names, dates.
3. **Main Findings / Highlights** – most significant points.
4. **Notable Details** – anything critical or unusual.
5. **Potential Concerns or Gaps** – anything missing, risky, or ambiguous.
6. **Summary & Next Steps** – brief summary and recommended actions.

Document:
{text}""",
    )


def run_pipeline(text: str):
    """Orchestrator: runs the agents in sequence, passing context along."""
    doc_type = classifier_agent(text)
    extraction = extractor_agent(text, doc_type)
    analysis = analyst_agent(text, doc_type, extraction)
    return doc_type, extraction, analysis


# ── Text extraction ───────────────────────────────────────────────────────────

def extract_document_text(uploaded_file):
    uploaded_file.seek(0)
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        reader = pypdf.PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8", errors="replace")
    else:
        st.error("Unsupported file type. Please upload a PDF or TXT file.")
        return None

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]
        st.info("Document was truncated to fit the model's context window.")
    return text


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("AI Document Analyser (Multi-Agent)")
st.caption("A classifier, an extractor (with tools), and an analyst work together on your document.")

uploaded_files = st.file_uploader(
    "Upload a document (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    docs_cache = st.session_state.setdefault("docs_cache", {})

    for file in uploaded_files:
        if file.name not in docs_cache:
            with st.spinner(f"Reading {file.name}..."):
                text = extract_document_text(file)
            if text is None:
                continue
            with st.spinner(f"Classifying {file.name}..."):
                doc_type = classifier_agent(text)
            docs_cache[file.name] = {
                "text": text,
                "doc_type": doc_type,
                "extraction": None,
                "analysis": None,
            }

    type_to_files: dict[str, list[str]] = {}
    for file in uploaded_files:
        if file.name in docs_cache:
            type_to_files.setdefault(docs_cache[file.name]["doc_type"], []).append(file.name)

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
                    st.caption(f"Identified as a **{doc_type}**. Three agents will collaborate on the analysis.")

                    if st.button("Run Multi-Agent Analysis", key=f"btn_{fname}", type="primary", use_container_width=True):
                        try:
                            with st.spinner("Extractor agent gathering facts (with tools)..."):
                                cached["extraction"] = extractor_agent(cached["text"], doc_type)
                            with st.spinner("Analyst agent writing the report..."):
                                cached["analysis"] = analyst_agent(cached["text"], doc_type, cached["extraction"])
                        except Exception as e:
                            st.error(str(e))

                    if cached.get("extraction"):
                        with st.expander("🔎 Extractor agent output (tool-assisted)"):
                            st.markdown(cached["extraction"])
                    if cached.get("analysis"):
                        st.markdown(cached["analysis"])

                    st.markdown("---")
else:
    st.info("Upload one or more PDF or TXT files to get started.")