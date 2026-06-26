from typing import TypedDict
from langgraph.graph import StateGraph, END
 
# 1. Define state
class LessonState(TypedDict):
    topic: str
    lesson: str
    quiz: str
 
 
# 2. Create node 1
def create_lesson(state: LessonState):
    topic = state["topic"]
    lesson = f"Lesson created for topic: {topic}"
    return {"lesson": lesson}
 
 
# 3. Create node 2
def create_quiz(state: LessonState):
    lesson = state["lesson"]
    quiz = f"Quiz created based on: {lesson}"
    return {"quiz": quiz}
 
 
# 4. Build graph
graph = StateGraph(LessonState)
 
graph.add_node("lesson_node", create_lesson)
graph.add_node("quiz_node", create_quiz)
 
graph.set_entry_point("lesson_node")
graph.add_edge("lesson_node", "quiz_node")
graph.add_edge("quiz_node", END)
 
# 5. Compile graph
app = graph.compile()
 
# 6. Run graph
result = app.invoke({
    "topic": "Python Loops",
    "lesson": "",
    "quiz": ""
})
 
print(result)