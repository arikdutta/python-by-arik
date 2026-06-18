from langchain_core.prompts import PromptTemplate
template = """
Create a training plan for
Topic: {topic}
Duration: {duration}
"""
prompt = PromptTemplate(
   input_variables=["topic","duration"],
   template=template
)
print(
   prompt.format(
       topic="Python",
       duration="30 Days"
   )
)