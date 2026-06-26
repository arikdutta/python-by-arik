"""
Hiring Workflow — Agent-Based Architecture
==========================================
Refactor of the LangGraph node-based pipeline into autonomous agents.

Each "node" becomes an Agent: a self-contained object with a single
responsibility, an explicit input/output contract, and a `run()` method.
An Orchestrator wires the agents together and handles the conditional
routing that the original graph expressed via conditional edges.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


# =========================
# 1. SHARED STATE
# =========================
@dataclass
class HiringState:
    raw_candidate_text: str = ""
    name: str = ""
    experience: int = 0
    skills: List[str] = field(default_factory=list)
    expected_salary: int = 0
    fit_status: str = ""
    interview_questions: str = ""
    rejection_reason: str = ""
    final_summary: str = ""


# =========================
# 2. BASE AGENT
# =========================
class Agent(ABC):
    """Base class for all hiring agents."""

    name: str = "Agent"

    @abstractmethod
    def run(self, state: HiringState) -> HiringState:
        """Process the state and return the (mutated) state."""
        raise NotImplementedError


# =========================
# 3. RESUME PARSER AGENT
# =========================
class ResumeParserAgent(Agent):
    name = "ResumeParserAgent"

    def run(self, state: HiringState) -> HiringState:
        # In a real system this might call an LLM / resume parser.
        # Here we simulate structured extraction.
        state.name = "Rahul Sharma"
        state.experience = 3
        state.skills = ["Python", "SQL", "APIs"]
        state.expected_salary = 35000
        return state


# =========================
# 4. SALARY CHECK AGENT
# =========================
class SalaryCheckAgent(Agent):
    name = "SalaryCheckAgent"

    def run(self, state: HiringState) -> HiringState:
        benchmark_salary = (state.experience * 10000) + 10000
        state.fit_status = "Fit" if state.expected_salary <= benchmark_salary else "Unfit"
        return state


# =========================
# 5. INTERVIEW AGENT
# =========================
class InterviewAgent(Agent):
    name = "InterviewAgent"

    def run(self, state: HiringState) -> HiringState:
        skills = ", ".join(state.skills)
        state.interview_questions = f"""
Interview Questions for {state.name}:

Candidate Skills: {skills}
Experience: {state.experience} years

1. Explain one Python project you have worked on.
2. How do you work with APIs in Python?
3. How do you optimize SQL queries?
4. Tell us about a debugging challenge you solved.
5. How do you structure backend logic in a real project?
"""
        return state


# =========================
# 6. REJECTION AGENT
# =========================
class RejectionAgent(Agent):
    name = "RejectionAgent"

    def run(self, state: HiringState) -> HiringState:
        state.rejection_reason = (
            "Candidate salary expectation exceeds benchmark salary "
            "for the given experience level."
        )
        return state


# =========================
# 7. SUMMARY AGENT
# =========================
class SummaryAgent(Agent):
    name = "SummaryAgent"

    def run(self, state: HiringState) -> HiringState:
        header = f"""
========== FINAL HR SUMMARY ==========

Candidate Name: {state.name}
Experience: {state.experience} years
Skills: {", ".join(state.skills)}
Expected Salary: ₹{state.expected_salary}
Fit Status: {state.fit_status}
"""
        if state.fit_status == "Fit":
            state.final_summary = header + f"""
Interview Questions:
{state.interview_questions}
"""
        else:
            state.final_summary = header + f"""
Reason for Rejection:
{state.rejection_reason}
"""
        return state


# =========================
# 8. ORCHESTRATOR
# =========================
class HiringOrchestrator:
    """
    Coordinates the agents, replacing the LangGraph edges/router.
    """

    def __init__(self) -> None:
        self.parser = ResumeParserAgent()
        self.salary = SalaryCheckAgent()
        self.interview = InterviewAgent()
        self.rejection = RejectionAgent()
        self.summary = SummaryAgent()

    def run(self, state: HiringState) -> HiringState:
        state = self.parser.run(state)
        state = self.salary.run(state)

        # Conditional routing (was: conditional_edges + router)
        if state.fit_status == "Fit":
            state = self.interview.run(state)
        else:
            state = self.rejection.run(state)

        # Both paths merge into the summary agent
        state = self.summary.run(state)
        return state


# =========================
# 9. RUN WORKFLOW
# =========================
if __name__ == "__main__":
    initial_state = HiringState(
        raw_candidate_text="Rahul Sharma, 3 years Python developer, expected salary 35000"
    )

    orchestrator = HiringOrchestrator()
    result = orchestrator.run(initial_state)

    print(result.final_summary)