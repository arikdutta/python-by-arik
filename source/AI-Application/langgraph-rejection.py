from typing import TypedDict
from langgraph.graph import StateGraph, END
 
class CandidateState(TypedDict):
    experience: int
    expected_salary: int
    fit_status: str
    result: str
    
    
def salary_check(state: CandidateState):
    experience = state["experience"]
    expected_salary = state["expected_salary"]
 
    benchmark_salary = (experience * 10000) + 10000
 
    if expected_salary <= benchmark_salary:
        return {"fit_status": "Fit"}
    else:
        return {"fit_status": "Unfit"}
 
def interview_questions(state: CandidateState):
    return {"result": "Generate interview questions for candidate"}
 
def rejection_summary(state: CandidateState):
    return {"result": "Candidate salary expectation too high. Marked unfit."}
 
def route_candidate(state: CandidateState):
    if state["fit_status"] == "Fit":
        return "interview_node"
    else:
        return "reject_node"
 
 
graph = StateGraph(CandidateState)
 
graph.add_node("salary_node", salary_check)
graph.add_node("interview_node", interview_questions)
graph.add_node("reject_node", rejection_summary)
 
graph.set_entry_point("salary_node")
 
graph.add_conditional_edges(
    "salary_node",
    route_candidate
)
 
graph.add_edge("interview_node", END)
graph.add_edge("reject_node", END)
 
app = graph.compile()


result = app.invoke({
    "experience": 2,
    "expected_salary": 30000,
    "fit_status": "",
    "result": ""
})
 
print(result)