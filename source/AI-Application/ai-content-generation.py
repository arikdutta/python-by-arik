import streamlit as st
st.title(
   "AI Content Generator"
)
topic = st.text_input(
   "Topic"
)
if st.button("Generate"):
   st.write(
       f"Blog on {topic}"
   )