from langchain_core.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.environ.get("ANTHROPIC_API_KEY")
template = """
 
Create a complete training plan
 
Topic: {topic}
 
Audience: {audience}
 
Duration: {duration}
 
"""
 
prompt = PromptTemplate(
 
    input_variables=[
 
        "topic",
 
        "audience",
 
        "duration"
 
    ],
 
    template=template
 
)
 
result = prompt.format(
 
    topic="Generative AI",
 
    audience="Corporate Employees",
 
    duration="5 Days"
 
)

 
llm = ChatAnthropic(
    model="claude-opus-4-8",
    api_key=api_key
)
 
response = llm.invoke(result)
 
print(response.content)
 