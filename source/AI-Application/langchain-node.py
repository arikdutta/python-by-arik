from typing import TypedDict, List
from langgraph.graph import StateGraph, END
 
 
# =========================
# 1. DEFINE STATE
# =========================
class HiringState(TypedDict):
    raw_candidate_text: str
    name: str
    experience: int
    skills: List[str]
    expected_salary: int
    fit_status: str
    interview_questions: str
    rejection_reason: str
    final_summary: str
 
 
# =========================
# 2. NODE 1 - RESUME PARSE NODE
# =========================
def resume_parse_node(state: HiringState):
    """
    Simulates extracting structured candidate information
    from raw candidate input text.
    """
 
    # In real system this may use LLM / parser / resume extractor
    # Here we simulate structured extraction
    return {
        "name": "Rahul Sharma",
        "experience": 3,
        "skills": ["Python", "SQL", "APIs"],
        "expected_salary": 35000
    }
 
 
# =========================
# 3. NODE 2 - SALARY CHECK NODE
# =========================
def salary_check_node(state: HiringState):
    """
    Checks whether expected salary is within benchmark range
    based on years of experience.
    """
 
    experience = state["experience"]
    expected_salary = state["expected_salary"]
 
    benchmark_salary = (experience * 10000) + 10000
 
    if expected_salary <= benchmark_salary:
        return {"fit_status": "Fit"}
    else:
        return {"fit_status": "Unfit"}
 
 
# =========================
# 4. NODE 3 - INTERVIEW NODE
# =========================
def interview_node(state: HiringState):
    """
    Generates interview questions if candidate is fit.
    """
 
    name = state["name"]
    experience = state["experience"]
    skills = ", ".join(state["skills"])
 
    questions = f"""
Interview Questions for {name}:
 
Candidate Skills: {skills}
Experience: {experience} years
 
1. Explain one Python project you have worked on.
2. How do you work with APIs in Python?
3. How do you optimize SQL queries?
4. Tell us about a debugging challenge you solved.
5. How do you structure backend logic in a real project?
"""
 
    return {
        "interview_questions": questions
    }
 
 
# =========================
# 5. NODE 4 - REJECTION NODE
# =========================
def rejection_node(state: HiringState):
    """
    Generates rejection reason if candidate is unfit.
    """
 
    return {
        "rejection_reason": "Candidate salary expectation exceeds benchmark salary for the given experience level."
    }
 
 
# =========================
# 6. NODE 5 - FINAL SUMMARY NODE
# =========================
def final_summary_node(state: HiringState):
    """
    Creates final HR summary using fit/unfit path outputs.
    """
 
    if state["fit_status"] == "Fit":
        summary = f"""
========== FINAL HR SUMMARY ==========
 
Candidate Name: {state['name']}
Experience: {state['experience']} years
Skills: {", ".join(state['skills'])}
Expected Salary: ₹{state['expected_salary']}
Fit Status: {state['fit_status']}
 
Interview Questions:
{state['interview_questions']}
"""
    else:
        summary = f"""
========== FINAL HR SUMMARY ==========
 
Candidate Name: {state['name']}
Experience: {state['experience']} years
Skills: {", ".join(state['skills'])}
Expected Salary: ₹{state['expected_salary']}
Fit Status: {state['fit_status']}
 
Reason for Rejection:
{state['rejection_reason']}
"""
 
    return {"final_summary": summary}
 
 
# =========================
# 7. ROUTER FUNCTION
# =========================
def route_candidate(state: HiringState):
    """
    Decides next node after salary check.
    """
    if state["fit_status"] == "Fit":
        return "interview_node"
    return "rejection_node"
 
 
# =========================
# 8. BUILD GRAPH
# =========================
graph = StateGraph(HiringState)
 
graph.add_node("resume_parse_node", resume_parse_node)
graph.add_node("salary_check_node", salary_check_node)
graph.add_node("interview_node", interview_node)
graph.add_node("rejection_node", rejection_node)
graph.add_node("final_summary_node", final_summary_node)
 
# Entry point
graph.set_entry_point("resume_parse_node")
 
# Normal edge
graph.add_edge("resume_parse_node", "salary_check_node")
 
# Conditional edge
graph.add_conditional_edges(
    "salary_check_node",
    route_candidate,
    {
        "interview_node": "interview_node",
        "rejection_node": "rejection_node"
    }
)
 
# Both paths merge into final summary
graph.add_edge("interview_node", "final_summary_node")
graph.add_edge("rejection_node", "final_summary_node")
 
# End
graph.add_edge("final_summary_node", END)
 
# Compile
app = graph.compile()
 
 
# =========================
# 9. RUN WORKFLOW
# =========================
result = app.invoke({
    "raw_candidate_text": "Rahul Sharma, 3 years Python developer, expected salary 35000",
    "name": "",
    "experience": 0,
    "skills": [],
    "expected_salary": 0,
    "fit_status": "",
    "interview_questions": "",
    "rejection_reason": "",
    "final_summary": ""
})
 
print(result["final_summary"])